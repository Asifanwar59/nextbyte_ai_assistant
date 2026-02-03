import requests
import os
from pathlib import Path
from .rag_engine import get_rag_context

# Example using HeyGen API (popular in 2026 for educational avatars)
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
VIDEO_OUTPUT_DIR = Path("data/videos")


async def generate_lesson_video(user_query: str, subject: str):
    # 1. Retrieve educational context from your RAG engine
    context = get_rag_context(user_query)

    # 2. Refine the context into a 30-minute student-friendly script
    # You would typically use an LLM here to format 'context' into 'video_script'
    video_script = f"Hello Class 8! Today we are learning about {subject}. {context}"

    # 3. Trigger AI Video Generation
    payload = {
        "video_settings": {
            "avatar_id": "classroom_teacher_01",
            "voice_id": "en_us_teacher_male",
            "style": "educational"
        },
        "script": video_script,
        "title": f"Lesson: {user_query[:30]}"
    }

    headers = {
        "X-Api-Key": HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.heygen.com", json=payload, headers=headers)

    if response.status_code == 200:
        video_id = response.json().get("video_id")
        return {"status": "processing", "video_id": video_id}
    else:
        return {"status": "error", "message": "Video generation failed"}
