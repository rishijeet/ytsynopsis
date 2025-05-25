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
async def transcribe_ui(request: Request, file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            result = model.transcribe(tmp.name)
            transcript = result["text"]
        os.unlink(tmp.name)

        # Debug print to verify transcript
        print(f"DEBUG - Transcript: {transcript}")

        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request,
                "transcript": transcript
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error": str(e)}
        )

# New endpoint for progress updates
@app.get("/progress")
async def get_progress():
    return {"progress": 0}  # Frontend will poll this
