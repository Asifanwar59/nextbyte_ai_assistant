#from django.db.models.expressions import result
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os


from .services.rag_engine import get_rag_context
from fastapi.middleware.cors import CORSMiddleware


FOTOR = True
HEYGEN = False

if HEYGEN:
    from .services.heygen_video_service import generate_lesson_video as video_service
elif FOTOR:
    from .services.fotor_service import generate_fotor_lesson as video_service
app = FastAPI()
# Define the local path
UPLOAD_DIR = Path("data/uploads")


# Add this middleware to allow your frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
# 1. Define what the incoming data looks like
class ChatRequest(BaseModel):
    query: str

'''
@app.post("/api/chat")
async def chat(query: str):
    return {"answer": f"Processed: {query}"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # 2. Extract the query text from the model
    user_query = request.query

    # 3. Integrate your RAG logic here (Example)
    result = rag_engine.query(user_query)
    answer = result["answer"]

    return {"answer": f"Processed: {user_query}"}
'''


@app.post("/api/chat")
async def chat(request: ChatRequest):
    # 1. Retrieve the custom knowledge from your PDFs

    # Pending actions: uncomment and add api keys and re-build
    # context = get_rag_context(request.query)
    # 2. (Optional) Pass this context to your LLM prompt
    # response = llm.generate(prompt=f"Context: {context}\nQuestion: {request.query}")
    #return {"answer": f"Retrieved Context: {context[:200]}..."}

    # Temporarily bypassing the LLM call for testing frontend:
    # Access the query using request.query
    return {"answer": f"Processed: {request.query}"}


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

@app.post("/api/generate-lesson")
async def create_lesson(query: str, subject: str, background_tasks: BackgroundTasks):
    # Videos take time to generate, so we run this as a background task
    #background_tasks.add_task(generate_lesson_video, query, subject)
    background_tasks.add_task(video_service, query, subject)
    return {"message": "Video generation started. It will appear in the classroom stream shortly."}