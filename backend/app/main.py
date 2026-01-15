from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# STEP 1: Define the app object FIRST
app = FastAPI()

# STEP 2: Configure Middleware (Optional but recommended for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# STEP 3: Now you can use @app
@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.post("/chat")
async def chat(query: str):
    # Your logic here
    return {"answer": "Received query: " + query}

# If you have an upload endpoint
@app.post("/upload")
async def upload_file():
    return {"status": "success"}
