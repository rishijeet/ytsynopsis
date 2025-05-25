import whisper
import os

model_size = os.getenv("WHISPER_MODEL", "base")
print(f"Downloading {model_size} model...")
whisper.load_model(model_size)
print("Model downloaded successfully")
