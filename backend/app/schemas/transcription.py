from pydantic import BaseModel

class TranscriptResponse(BaseModel):
    text: str
    status: str
