
import os
import json
from datetime import datetime
import yt_dlp
import whisper

def log(msg):
    print(f"[whisper_transcriber] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def download_youtube_audio(url, output_path="audio.mp3"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(model, audio_path):
    return model.transcribe(audio_path)

def save_transcript(result, video_id):
    os.makedirs("data", exist_ok=True)
    output_path = f"data/transcript_{video_id}.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    log(f"Saved transcript to {output_path}")

if __name__ == "__main__":
    log("Starting YouTube Arabic transcription...")

    youtube_links = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/@hamdyandwafaa",
        "https://www.youtube.com/@hamdyandwafaa2",
        "https://www.youtube.com/@Bjlifeز"
    ]

    model = whisper.load_model("base")

    for url in youtube_links:
        try:
            log(f"Downloading video: {url}")
            video_id = url.split("/")[-1]
            audio_path = f"temp_{video_id}.mp3"
            download_youtube_audio(url, output_path=audio_path)
            log("Transcribing with Whisper...")
            result = transcribe_audio(model, audio_path)
            save_transcript(result, video_id)
            os.remove(audio_path)
        except Exception as e:
            log(f"❌ Failed on {url}: {e}")

    log("Finished transcription pipeline.")
