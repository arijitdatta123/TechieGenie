from fastapi import APIRouter, UploadFile, File
from stt.stt import speech_to_text
from llm.chain import ask_llm
from tts.tts import text_to_speech
import uuid
import os

router = APIRouter()

@router.post("/chat/voice")
async def chat_voice(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    # 1. STT
    user_text = speech_to_text(audio_bytes)

    # 2. LLM with video_id
    llm_result = ask_llm(user_text)
    answer = llm_result["answer"]
    video_id = llm_result.get("video_id")

    # 3. Convert answer → speech
    audio_data = text_to_speech(answer)
    audio_filename = f"{uuid.uuid4()}.wav"
    audio_path = f"static/audio/{audio_filename}"

    with open(audio_path, "wb") as f:
        f.write(audio_data)

    # 4. Prepare video URL
    video_url = None
    if video_id:
        video_path = f"static/videos/{video_id}.mp4"
        if os.path.exists(video_path):
            video_url = f"/static/videos/{video_id}.mp4"

    return {
        "answer": answer,
        "audio_url": f"/static/audio/{audio_filename}",
        "video_url": video_url
    }
