YouTube Transcriber
This project allows you to download audio from YouTube videos or playlists and transcribe them using OpenAI’s Whisper model.

Features
Download audio from YouTube videos and playlists (via yt-dlp)
Transcribe audio to text (via OpenAI's Whisper with CPU-only processing)
Saves each transcript as a text file alongside the audio file
Requirements
Python 3.7+
Apple Silicon Mac (M1 or later)
The following Python libraries:
yt-dlp
whisper
torch
Setup
1. Clone the Repository
git clone https://github.com/YourUsername/m1_youtube_transcriber.git
cd m1_youtube_transcriber
2. Set Up a Virtual Environment
Create and activate a virtual environment to isolate the dependencies for this project.

python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
3. Install the Required Libraries
Install the necessary Python packages using pip.

pip install yt-dlp whisper torch
Usage
Running the Script
After setting up the environment, you can use the script to transcribe a single video or an entire playlist.

For a Single Video
python m1_youtube_transcriber_suppress_warnings.py --video "YOUTUBE_VIDEO_URL"
For a Playlist
python m1_youtube_transcriber_suppress_warnings.py --playlist "YOUTUBE_PLAYLIST_URL"
Replace YOUTUBE_VIDEO_URL or YOUTUBE_PLAYLIST_URL with the URL of the YouTube video or playlist you want to transcribe.

Output
Audio Files: Saved in the downloads/ directory as .wav files.
Transcripts: Saved in the downloads/ directory with _transcript.txt suffix for each video.
Example
python m1_youtube_transcriber_suppress_warnings.py --video "https://www.youtube.com/watch?v=xvFZjo5PgG0"
Troubleshooting
If you encounter issues, make sure:

All dependencies are installed in the virtual environment.
You are running the script in the virtual environment.
For other issues related to YouTube API or Whisper model warnings, this script suppresses most non-critical warnings for cleaner output.

License
This project is open-source and available for modification.
