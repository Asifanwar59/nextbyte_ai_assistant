import os
import requests
from pathlib import Path

# Note: As of 2026, FlexClip primarily uses web-based automation or API triggers
# for their "Text-to-Video" Creation Mode.
FLEXCLIP_API_KEY = os.getenv("FLEXCLIP_API_KEY")


async def generate_flexclip_lesson(query: str, script_content: str):
    """
    Triggers FlexClip's AI Excerpt Mode to convert RAG scripts
    into formatted lesson videos for Grade 8.
    """
    endpoint = "https://api.flexclip.com"

    # FlexClip AI Creation Mode automatically matches stock footage,
    # adds subtitles, and overlays AI voiceovers.
    payload = {
        "mode": "AI_EXCERPT",
        "script": script_content,
        "aspect_ratio": "16:9",
        "voice_settings": {
            "language": "en-US",
            "voice_id": "neural_friendly_teacher",  # 400+ voices available
            "speed": 1.0
        },
        "style": "educational_presentation",
        "output_resolution": "1080p"  # Business plans support 4K
    }

    headers = {"Authorization": f"Bearer {FLEXCLIP_API_KEY}"}

    response = requests.post(endpoint, json=payload, headers=headers)
    return response.json()  # Returns video_id or download_url
