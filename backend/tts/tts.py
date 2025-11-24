import uuid
import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

AUDIO_DIR = os.path.join("static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech(text):
    # 1️⃣ Delete old bot audio files
    for f in os.listdir(AUDIO_DIR):
        if f.startswith("bot_") and f.endswith(".wav"):
            try:
                os.remove(os.path.join(AUDIO_DIR, f))
            except:
                pass

    # 2️⃣ Generate new filename
    filename = f"bot_{uuid.uuid4()}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)

    # 3️⃣ Request TTS audio (binary)
    result = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    # 4️⃣ Save audio bytes
    audio_bytes = result.read()
    with open(filepath, "wb") as f:
        f.write(audio_bytes)

    # 5️⃣ Return file path for frontend
    return f"/static/audio/{filename}"
