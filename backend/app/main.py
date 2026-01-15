from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

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
