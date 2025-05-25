from pydantic import BaseModel, HttpUrl, validator

class YouTubeRequest(BaseModel):
    url: str
    
    @validator('url')
    def validate_youtube_url(cls, v):
        if 'youtube.com/watch?v=' not in v and 'youtu.be/' not in v:
            raise ValueError("Invalid YouTube URL")
        return v
