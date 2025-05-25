
# YouTube Video Summarizer

A Python-based tool that automatically summarizes YouTube video content using Whisper speech recognition and AI-powered NLP.
# Copyright (c) 2025 Rishijeet Mishra

## Features
- 🎥 Extract audio from YouTube videos
- 🎤 Convert speech to text using Whisper
- ✂️ Generate concise summaries with NLP
- 🚀 FastAPI backend with modern UI

## Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/rishijeet/ytsynopsis.git
   cd ytsynopsis
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Access at: http://localhost:8000

## Project Structure

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface for file upload |
| `/transcribe` | POST | Process audio file (returns JSON) |

## API Usage
```bash
POST /summarize
Body: { "youtube_url": "https://youtube.com/watch?v=..." }
```

## Contributing
Pull requests welcome! For major changes, please open an issue first.

## License
MIT
