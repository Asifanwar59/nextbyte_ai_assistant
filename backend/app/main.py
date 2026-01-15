from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()
# Define the local path
UPLOAD_DIR = Path("data/uploads")


def process_local_pdfs():
    """Scans the local directory and processes any PDFs found."""
    if not UPLOAD_DIR.exists():
        print(f"Directory {UPLOAD_DIR} does not exist.")
        return

    processed_files = []
    for file_path in UPLOAD_DIR.glob("*.pdf"):
        # Replace the logic below with your actual RAG indexing/processing logic
        print(f"Processing: {file_path.name}")
        # index_document(file_path)
        processed_files.append(file_path.name)

    return processed_files

@app.post("/process-internal-data")
async def trigger_processing(background_tasks: BackgroundTasks):
    """Endpoint for the frontend to trigger a re-scan of the local data folder."""
    background_tasks.add_task(process_local_pdfs)
    return {"message": "Processing of local data/uploads started in background."}

# Optional: Process files automatically on startup
@app.on_event("startup")
async def startup_event():
    process_local_pdfs()

# --- API Endpoints ---
@app.post("/api/chat")
async def chat(query: str):
    return {"answer": f"Processed: {query}"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    return {"filename": file.filename}

# --- Serve React Frontend ---
# 1. Mount the 'static' directory for JS/CSS files
# Ensure this folder exists or is created during Docker build
app.mount("/assets", StaticFiles(directory="app/static/assets"), name="assets")

# 2. Catch-all route to serve index.html for the React SPA
@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    # This ensures that if you refresh the page on a sub-route, it still works
    return FileResponse("app/static/index.html")
