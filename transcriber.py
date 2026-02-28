import os
import imageio_ffmpeg
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

from transformers import pipeline

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file using Hugging Face's distil-whisper model.
    This model runs much faster on CPU than the standard openai-whisper models.
    """
    # We use chunk_length_s to handle long audio files (e.g., larger than 30 seconds)
    transcriber = pipeline(
        "automatic-speech-recognition", 
        model="distil-whisper/distil-small.en",
        chunk_length_s=30
    )
    
    # Perform transcription
    result = transcriber(file_path)
    
    return result["text"]
