import ffmpeg
import os

def convert_to_wav(input_path: str, output_path: str):
    """Convert any audio to 16kHz mono WAV"""
    (
        ffmpeg
        .input(input_path)
        .output(output_path, ar=16000, ac=1)
        .run(quiet=True)
    )
