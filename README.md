
# YouTube Summarizer

A Python-based tool that automatically summarizes YouTube  content using Whisper speech recognition and AI-powered NLP. I have built this with the use case wherein I can get text/summary of amazing podcast, interviews, videos and keynotes and then using LLM can get crux of their point of views. 

<img width="1255" alt="Screenshot 2025-05-25 at 9 21 51 PM" src="https://github.com/user-attachments/assets/5883702d-495b-43ce-b57e-08e02aec7413" />

<img width="1209" alt="Screenshot 2025-05-25 at 9 21 24 PM" src="https://github.com/user-attachments/assets/c3a0b348-5493-4c71-a616-7b09e6fd99a4" />



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
