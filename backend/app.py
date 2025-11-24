from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from stt.stt import speech_to_text
from llm.chain import ask_llm
from tts.tts import text_to_speech
from llm.video_map import VIDEO_MAP

import os
app = FastAPI()
from fastapi.staticfiles import StaticFiles

# Serve /static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/chat/voice")
async def voice_chat(file: UploadFile = File(...)):
    # 1. Audio bytes
    audio_bytes = await file.read()

    # 2. Speech → Text
    user_text = speech_to_text(audio_bytes)

    # 3. LLM result
    llm_result = ask_llm(user_text)
    answer = llm_result["answer"]
    video_id = llm_result.get("video_id")

    # 4. Text → Speech (returns URL)
    audio_url = text_to_speech(answer)     # <-- FIXED ✔✔

    # 5. Resolve video
    video_url = None
    if video_id and video_id in VIDEO_MAP:
        filename = VIDEO_MAP[video_id]
        video_path = f"static/videos/{filename}"
        if os.path.exists(video_path):
            video_url = f"/static/videos/{filename}"


    return {
        "user_text": user_text,
        "answer": answer,
        "audio_url": audio_url,
        "video_url": video_url
    }


@app.get("/")
def root():
    return {"message": "Techigenie Backend Running"}
