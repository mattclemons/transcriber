import os
import subprocess
import argparse
from yt_dlp import YoutubeDL

def download_audio(video_url, output_path="downloads"):
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

    print(f"Downloading audio from {video_url}...")
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')

    print(f"Downloaded and saved as {audio_file}")

    # Resample the audio to 16 kHz
    resampled_audio_file = audio_file.replace(".wav", "_16k.wav")
    resample_command = ["ffmpeg", "-i", audio_file, "-ar", "16000", resampled_audio_file, "-y"]
    subprocess.run(resample_command)
    
    print(f"Resampled audio saved as {resampled_audio_file}")
    return audio_file, resampled_audio_file

def transcribe_audio_whisper_cpp(audio_file, model="large-v1"):
    model_path = f"/Users/mattclemons/git/whisper.cpp/models/ggml-{model}.bin"
    
    # Define the output file name
    transcript_file = audio_file.replace("_16k.wav", "_transcript.txt")
    
    # Command to run whisper.cpp without GPU flag, as it should auto-detect GPU support
    command = [
        "/Users/mattclemons/git/whisper.cpp/main",
        "-m", model_path,
        "-f", audio_file,
        "-otxt",  # Output in .txt format directly
        "-of", transcript_file,  # Directly specify output file name
        "-nt",    # No timestamps
        "-np"     # No progress printing in the console
    ]
    
    print(f"Transcribing {audio_file} using {model} model...")
    result = subprocess.run(command, capture_output=True, text=True)

    print(f"Clean transcription saved to {transcript_file}")
    return transcript_file

def cleanup_files(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted file: {file}")
        else:
            print(f"File not found, skipping: {file}")

def process_single_video(video_url, model="large-v1"):
    original_audio, resampled_audio = download_audio(video_url)
    transcript = transcribe_audio_whisper_cpp(resampled_audio, model=model)
    
    # Cleanup audio files and any potential duplicate transcript files
    cleanup_files(original_audio, resampled_audio, resampled_audio + ".txt")
    
    print(f"Completed transcription for video: {transcript}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Video Transcriber using whisper.cpp")
    parser.add_argument("--video", type=str, help="URL of the YouTube video to transcribe")
    parser.add_argument("--model", type=str, default="large-v1", help="Model size (e.g., tiny, base, small, medium, large, large-v1)")
    args = parser.parse_args()

    if args.video:
        process_single_video(args.video, model=args.model)
    else:
        print("Please provide a video URL using the --video argument.")

