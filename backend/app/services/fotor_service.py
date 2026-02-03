import os
import requests
from pathlib import Path

FOTOR_API_KEY = os.getenv("FOTOR_API_KEY")
VIDEO_DIR = Path("data/videos")


async def generate_fotor_lesson(topic: str, context: str):
    """
    Uses Fotor's Text-to-Video API to create educational content
    for Class 8 students.
    """
    endpoint = "https://api.fotor.com"

    # Constructing a structured prompt for Fotor's AI
    payload = {
        "text": f"Create an educational lesson for 14-year-olds about {topic}. Content: {context[:500]}",
        "aspect_ratio": "16:9",
        "video_style": "educational_animation",  # Fotor's preset for classroom clarity
        "voice_over": {
            "enabled": True,
            "voice_name": "Teacher_Marcus",  # 2026 high-clarity neural voice
            "language": "en-US"
        },
        "resolution": "1080p",
        "auto_subtitles": True
    }

    headers = {
        "Authorization": f"Bearer {FOTOR_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    data = response.json()

    # In 2026, Fotor usually returns a job_id for asynchronous processing
    return {"job_id": data.get("job_id"), "status": "processing"}
