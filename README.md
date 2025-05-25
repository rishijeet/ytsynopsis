
# YouTube Summarizer

A Python-based tool that automatically summarizes YouTube  content using Whisper speech recognition and AI-powered NLP. I have built this with the use case wherein I can get text/summary of amazing podcast, interviews, videos and keynotes and then using LLM can get crux of their point of views. 

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
   ```
## Copyright
2025 Rishijeet Mishra. MIT License