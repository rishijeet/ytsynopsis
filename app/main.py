"""
YouTube Video Summarizer
Copyright (c) 2025 Rishijeet Mishra
"""

from fastapi import FastAPI, UploadFile, HTTPException, File, Request, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import whisper
import tempfile
import os
from dotenv import load_dotenv
import logging
from pydantic import BaseModel
import time
from app.utils.youtube import download_audio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Disable noisy logs
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# Initialize FastAPI app
app = FastAPI(title="Audio Transcription API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Mount static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates (HTML)
templates = Jinja2Templates(directory="templates")

# Load Whisper model
model = whisper.load_model(os.getenv("WHISPER_MODEL", "base"))

# Response model
class TranscriptionResponse(BaseModel):
    text: str
    language: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcribe", response_class=HTMLResponse)
async def transcribe(request: Request, youtube_url: str = Form(...)):
    start_time = time.time()  # Start timer (can be removed if not needed elsewhere)
    
    try:
        if not youtube_url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format")
            
        audio_path, video_title, video_duration, upload_date = download_audio(youtube_url)
        
        try:
            result = model.transcribe(audio_path)
            os.unlink(audio_path)
            
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "transcript": result["text"],
                    "video_title": video_title,
                    "video_duration": video_duration,
                    "upload_date": upload_date
                }
            )
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)
                temp_dir = os.path.dirname(audio_path)
                if temp_dir.startswith(tempfile.gettempdir()):
                    try:
                        os.rmdir(temp_dir)
                    except OSError:
                        pass
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(e)},
            status_code=400
        )

# New endpoint for progress updates
@app.get("/progress")
async def get_progress():
    return {"progress": 0}  # Frontend will poll this
