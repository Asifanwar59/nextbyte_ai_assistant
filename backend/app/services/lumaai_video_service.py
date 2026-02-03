import os
import time
from lumaai import LumaAI
from pathlib import Path

# Initialize Luma AI Client
luma_client = LumaAI(api_key=os.getenv("LUMAAI_API_KEY"))
VIDEO_DIR = Path("data/videos")


async def generate_luma_lesson(topic: str, context: str):
    """
    Generates a high-fidelity educational video using Luma AI Ray3.
    """
    # 1. Create the cinematic educational prompt
    # Luma Ray3 allows for high character and scene consistency
    prompt = (
        f"Cinematic educational tutorial for class 8 students on {topic}. "
        f"Visualizing: {context[:200]}. Photorealistic, 4k, smooth camera motion, "
        "professional lighting."
    )

    # 2. Start the generation
    generation = luma_client.generations.create(
        prompt=prompt,
        aspect_ratio="16:9",
        loop=False  # Lessons are linear, not looping
    )

    # 3. Poll for completion (Luma is ID-based)
    while True:
        status = luma_client.generations.get(id=generation.id)
        if status.state == "completed":
            video_url = status.assets.video
            break
        elif status.state == "failed":
            raise Exception("Luma AI generation failed.")
        time.sleep(5)  # Poll every 5 seconds

    return {"video_url": video_url, "id": generation.id}
