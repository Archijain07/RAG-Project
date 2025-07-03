from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Tuple
from ingestion import run_ingestion, parse_page_range_input
from ask_pdf import answer_question

app = FastAPI()

class IngestionRequest(BaseModel):
    url: str
    chunk_type: str = "recursive"
    page_range: str = "1-3"  # e.g., "1-5"

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "🚀 Welcome to the PDF QA API!"}

@app.post("/ingest")
def ingest_pdf(data: IngestionRequest):
    if data.page_range.strip().lower() == "all":
        page_range = None
    else:
        page_range = parse_page_range_input(data.page_range)
        if not page_range:
            return {"error": "❌ Invalid page range format. Use format like 1-3 or 'all'."}

    run_ingestion(url=data.url, chunk_type=data.chunk_type, page_range=page_range)
    return {"status": "✅ Ingestion complete"}


@app.post("/ask")
def ask_question(data: QuestionRequest):
    if not data.question.strip():
        return {"error": "❌ Question cannot be empty."}
    answer = answer_question(data.question)
    return {"question": data.question, "answer": answer}
