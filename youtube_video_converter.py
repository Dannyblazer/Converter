import os
from typing import Optional
from pytube import YouTube
from moviepy.editor import AudioFileClip
from pytube.cli import on_progress


def download_audio(url: str, output_path: str = '.') -> Optional[str]:
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if audio_stream is None:
            print("No audio stream found.")
            return None
        
        print(f"Downloading: {yt.title}")
        output_file: str = audio_stream.download(output_path)
        print(f"Downloaded: {yt.title}")

        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None

def convert_to_mp3(audio_file: str) -> None:
    try:
        base, _ = os.path.splitext(audio_file)
        mp3_file: str = f"{base}.mp3"

        with AudioFileClip(audio_file) as audio_clip:
            audio_clip.write_audiofile(mp3_file)

        os.remove(audio_file)  # Remove the original audio file
        print(f"Converted to MP3: {mp3_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_url: str = input("Enter the YouTube video URL: ")
    output_path: str = input("Enter the output path (leave empty for current directory): ") or '.'
    
    downloaded_file: Optional[str] = download_audio(video_url, output_path)
    if downloaded_file:
        convert_to_mp3(downloaded_file)

