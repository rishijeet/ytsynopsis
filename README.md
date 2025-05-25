# Audio Transcription API

A FastAPI backend for audio-to-text transcription using OpenAI's Whisper model.

## Features
- 🎤 Upload MP3 files and get text transcripts
- ⚡ FastAPI backend with async processing
- 🔍 Powered by OpenAI's Whisper (offline)
- 📁 Progress tracking for long audio files

## Prerequisites
- Python 3.8+
- GPU recommended (but works on CPU)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/audio-transcription.git
   cd audio-transcription
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server
```bash
uvicorn app.main:app --reload
```
Access the web interface at: http://localhost:8000

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface for file upload |
| `/transcribe` | POST | Process audio file (returns JSON) |


