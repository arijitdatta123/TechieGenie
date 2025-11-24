from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def speech_to_text(audio_bytes):
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)

    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=open("temp.wav", "rb"),
        language="en"     # ✔ force English output
    )

    return result.text
