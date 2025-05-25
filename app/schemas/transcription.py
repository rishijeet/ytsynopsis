"""
YouTube Video Summarizer
Copyright (c) 2025 Rishijeet Mishra
"""
from pydantic import BaseModel

class TranscriptResponse(BaseModel):
    text: str
    status: str
