
import os
import whisper
import torch
import warnings
from yt_dlp import YoutubeDL
from datetime import datetime

# Suppress specific warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
warnings.filterwarnings("ignore", category=FutureWarning, message="You are using `torch.load` with `weights_only=False`")

def download_audio(video_url, output_path="downloads"):
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Set up yt-dlp options for audio-only download
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    # Download video as audio
    print(f"Downloading audio from {video_url}...")
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
    
    print(f"Downloaded and saved as {audio_file}")
    return audio_file

def transcribe_audio(audio_file):
    # Set device to CPU only for stable execution
    device = "cpu"
    model = whisper.load_model("base", device=device)
    
    # Transcribe audio
    print(f"Transcribing {audio_file} on {device}...")
    result = model.transcribe(audio_file)
    
    # Save the transcription to a file
    transcript_filename = os.path.splitext(audio_file)[0] + "_transcript.txt"
    with open(transcript_filename, "w") as f:
        f.write(result["text"])
    
    print(f"Transcription saved to {transcript_filename}")
    return transcript_filename

def process_single_video(video_url):
    audio_file = download_audio(video_url)
    transcript = transcribe_audio(audio_file)
    print(f"Completed transcription for video: {transcript}")

def process_playlist(playlist_url):
    print(f"Processing playlist: {playlist_url}")
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': True,
    }

    # Extract playlist items using yt-dlp
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        if "entries" in info_dict:
            video_urls = [entry['url'] for entry in info_dict['entries']]
        else:
            print("Failed to retrieve playlist contents.")
            return
    
    for video_url in video_urls:
        process_single_video(video_url)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YouTube Video/Playlist Transcriber using yt-dlp with CPU-based Whisper transcription")
    parser.add_argument("--video", type=str, help="URL of the single YouTube video to transcribe")
    parser.add_argument("--playlist", type=str, help="URL of the YouTube playlist to transcribe")

    args = parser.parse_args()

    if args.video:
        process_single_video(args.video)
    elif args.playlist:
        process_playlist(args.playlist)
    else:
        print("Please provide either a --video or --playlist URL")
