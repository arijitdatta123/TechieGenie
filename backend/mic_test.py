import sounddevice as sd
from scipy.io.wavfile import write
import uuid
import os
import winsound

from stt.stt import speech_to_text
from llm.chain import ask_llm
from tts.tts import text_to_speech
from llm.video_map import VIDEO_MAP


# 🎤 Record microphone input
def record_audio(duration=5, fs=44100):
    filename = f"mic_input_{uuid.uuid4()}.wav"
    print(f"\n🎤 Speak now... recording for {duration} seconds\n")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    write(filename, fs, recording)
    print(f"🎧 Audio saved: {filename}")

    return filename


# 🔊 Play WAV file
def play_audio(filename):
    print(f"\n🔊 Playing: {filename}\n")
    winsound.PlaySound(filename, winsound.SND_FILENAME)


# 🚀 MAIN PROCESS (STT → LLM → TTS → VIDEO)
def main():
    # 1️⃣ Record audio
    input_file = record_audio()

    # 2️⃣ Convert speech to text
    with open(input_file, "rb") as f:
        audio_bytes = f.read()

    print("\n📝 Converting speech to text...")
    text = speech_to_text(audio_bytes)
    print(f"User said: {text}")

    # 3️⃣ Ask LLM + RAG
    print("\n🧠 Asking LLM...")
    llm_result = ask_llm(text)
    print(f"LLM response: {llm_result}")

    # Extract answer + video ID
    answer_text = llm_result.get("answer")
    video_id = llm_result.get("video_id")

    # 4️⃣ Map video from backend
    if video_id and video_id in VIDEO_MAP:
        video_url = f"/static/{VIDEO_MAP[video_id]}"
    else:
        video_url = None

    print(f"\n🎬 Video to play: {video_url}")

    # 5️⃣ Generate TTS audio
    bot_audio = text_to_speech(answer_text)
    output_file = "bot_reply.wav"

    with open(output_file, "wb") as f:
        f.write(bot_audio)

    print(f"\n🔊 Bot reply saved as: {output_file}")

    # 6️⃣ Play bot voice
    play_audio(output_file)

    print("\n✅ Full pipeline complete!")


if __name__ == "__main__":
    main()
