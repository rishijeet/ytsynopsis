"""
YouTube Video Downloader
Copyright (c) 2025 Rishijeet Mishra
"""

import yt_dlp
import tempfile
import os
from pathlib import Path

def download_audio(youtube_url: str) -> tuple[str, str, str, str]:
    """Downloads YouTube audio and returns audio path, video title, duration, and upload date."""
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
            
            # Extract video metadata
            video_title = info.get('title', 'Untitled Video')
            video_duration = info.get('duration', 0)
            upload_date = info.get('upload_date', '')
            
            # Convert duration (seconds) to HH:MM:SS format
            hours, remainder = divmod(video_duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Format upload date (YYYYMMDD) to YYYY-MM-DD
            formatted_upload_date = (
                f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                if upload_date else 'Unknown'
            )
            
            return str(mp3_file), video_title, formatted_duration, formatted_upload_date
            
    except Exception as e:
        # Clean up temp files if they exist
        if 'temp_dir' in locals():
            for f in Path(temp_dir).glob('*'):
                f.unlink(missing_ok=True)
            Path(temp_dir).rmdir()
        raise Exception(f"Failed to download audio: {str(e)}")
