from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define request and response models using Pydantic
class TextRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: list

# Define the embedding generation endpoint
@app.post("/generate-embedding", response_model=EmbeddingResponse)
async def generate_embedding(request: TextRequest):
    text = request.text
    # Generate embedding using the pre-trained model
    embedding = model.encode(text)
    return EmbeddingResponse(embedding=embedding.tolist())

# Define a health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}