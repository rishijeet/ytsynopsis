from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import os
from dotenv import load_dotenv
import logging
from pydantic import BaseModel

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

# Load Whisper model
model = whisper.load_model(os.getenv("WHISPER_MODEL", "base"))

# Response model
class TranscriptionResponse(BaseModel):
    text: str
    language: str

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # Transcribe the audio
        result = model.transcribe(temp_file_path)
        transcription = result["text"]
        language = result.get("language", "en")

        # Clean up the temporary file
        os.unlink(temp_file_path)

        return {"text": transcription, "language": language}

    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))
