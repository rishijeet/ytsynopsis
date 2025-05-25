"""
YouTube Video Summarizer
Copyright (c) 2025 Rishijeet Mishra
"""
import whisper
import os
from tempfile import NamedTemporaryFile
from fastapi import UploadFile
from app.schemas.transcription import TranscriptResponse

model = whisper.load_model(os.getenv("WHISPER_MODEL", "base"))

async def transcribe_audio(file: UploadFile) -> TranscriptResponse:
    with NamedTemporaryFile(delete=True, suffix=".wav") as tmp:
        # Convert to WAV format (Whisper works best with 16kHz mono)
        contents = await file.read()
        tmp.write(contents)
        
        # Transcribe
        result = model.transcribe(tmp.name)
        return {
            "text": result["text"],
            "language": result["language"]
        }
