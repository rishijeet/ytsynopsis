"""
YouTube Video Downloader
Copyright (c) 2025 Rishijeet Mishra
"""

import yt_dlp
import tempfile
import os
from pathlib import Path

def download_audio(youtube_url: str) -> str:
    """Downloads YouTube audio with robust error handling"""
    try:
        temp_dir = tempfile.mkdtemp()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
            'no_warnings': True,
            'extractaudio': True,
            'audioformat': 'mp3'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            mp3_file = Path(downloaded_file).with_suffix('.mp3')
            
            if not mp3_file.exists():
                raise FileNotFoundError(f"FFmpeg failed to convert to MP3: {mp3_file}")
                
            return str(mp3_file)
            
    except Exception as e:
        # Clean up temp files if they exist
        if 'temp_dir' in locals():
            for f in Path(temp_dir).glob('*'):
                f.unlink(missing_ok=True)
            Path(temp_dir).rmdir()
        raise Exception(f"Failed to download audio: {str(e)}")
