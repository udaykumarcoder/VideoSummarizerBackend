# import os
# import subprocess
# from pytube import YouTube
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import TextFormatter
# from utils.vtt_parser import extract_plain_text

# def extract_video_id(url):
#     return YouTube(url).video_id

# def get_transcript(video_id, video_url=None):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         formatter = TextFormatter()
#         return formatter.format_transcript(transcript)
#     except Exception as e:
#         print("Transcript API failed:", str(e))
#         if video_url:
#             print("Trying fallback VTT method...")
#             return fallback_transcript_with_vtt(video_url)
#         raise e

# def fallback_transcript_with_vtt(video_url):
#     try:
#         subprocess.run([
#             "yt-dlp",
#             "--write-auto-sub", "--sub-lang", "en", "--skip-download",
#             "-o", "fallback.%(ext)s", video_url
#         ], check=True)

#         for file in os.listdir():
#             if file.endswith(".vtt") and "fallback" in file:
#                 text = extract_plain_text(file)
#                 os.remove(file)  # Clean up
#                 return text

#         raise FileNotFoundError("No fallback .vtt file found.")
#     except Exception as e:
#         raise RuntimeError(f"VTT fallback failed: {str(e)}")

import os
import re
import subprocess
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube

def extract_video_id(url):
    try:
        return YouTube(url).video_id
    except Exception as e:
        raise ValueError(f"Could not extract video ID: {str(e)}")

def get_transcript(video_id, video_url=None):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        text = formatter.format_transcript(transcript)
        save_transcript_to_file(text)
        return text
    except TranscriptsDisabled:
        print("Transcripts disabled or unavailable, trying fallback VTT method...")
        return fallback_download_vtt(video_url)
    except Exception as e:
        print("Primary method failed, trying fallback...")
        return fallback_download_vtt(video_url)

# ✅ FIXED: Accepts `video_url` instead of `video_id`
def fallback_download_vtt(video_url):
    filename = "fallback.en.vtt"

    try:
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "-o", "fallback.%(ext)s",
            video_url
        ], check=True)

        text = extract_plain_text(filename)
        save_transcript_to_file(text)
        return text
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to download subtitles with yt-dlp.")
    except Exception as e:
        raise RuntimeError(str(e))

def extract_plain_text(vtt_file_path):
    with open(vtt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    spoken_lines = []
    for line in lines:
        if re.match(r'\d\d:\d\d:\d\d\.\d+ -->', line):
            continue
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'align:start.*', '', line)
        line = line.strip()
        if line:
            spoken_lines.append(line)

    seen = set()
    cleaned = [x for x in spoken_lines if not (x in seen or seen.add(x))]
    return '\n'.join(cleaned)

def save_transcript_to_file(text, file_path="transcript.txt"):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(text)
    print(f"Transcript saved to {file_path}")

