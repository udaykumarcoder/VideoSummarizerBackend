import os
import requests
from dotenv import load_dotenv
from utils.yt_utils import extract_video_id, get_transcript

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_summary(video_link):
    video_id = extract_video_id(video_link)
    transcript = get_transcript(video_id, video_link)

    if not transcript:
        raise ValueError("No transcript available.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": f"Summarize this YouTube transcript:\n\n{transcript}"}
        ],
        "temperature": 0.5,
        "max_tokens": 8192,
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)
    response.raise_for_status()

    return transcript,response.json()["choices"][0]["message"]["content"]
