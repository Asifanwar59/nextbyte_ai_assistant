import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Initialize FastAPI (This is the "app" Uvicorn is looking for)
app = FastAPI()

# 2. Enable CORS so your frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize the Bedrock client
# Note: Ensure KnowledgeBaseId and ModelArn match your AWS setup
client = boto3.client('bedrock-agent-runtime', region_name='ap-south-2')

class ChatRequest(BaseModel):
    query: str

async def get_rag_response(query: str):
    response = client.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                # REPLACE 'YOUR_KB_ID' with your actual ID from AWS Console
                'knowledgeBaseId': 'YOUR_KB_ID',
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-v2:0'
            }
        }
    )
    return response['output']['text']

# 4. Define the API Endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        answer = await get_rag_response(request.query)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error calling AWS Bedrock: {str(e)}"}

# 5. Health Check for AWS Fargate
@app.get("/")
async def root():
    return {"status": "Nextbyte AI Assistant is online"}
