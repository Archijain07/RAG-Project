from fastapi import FastAPI, Query, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from ingestion import run_ingestion, parse_page_range_input
from ask_pdf import answer_question

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "🚀 Welcome to the PDF QA API!"}

@app.post("/ingest")
async def ingest_pdf(
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    chunk_type: str = Form("recursive"),
    page_range: str = Form("1-3")
):
    if not url and not file:
        return {"error": "❌ Provide either a URL or upload a PDF file."}

    if page_range.strip().lower() == "all":
        parsed_range = None
    else:
        parsed_range = parse_page_range_input(page_range)
        if not parsed_range:
            return {"error": "❌ Invalid page range format. Use format like 1-3 or 'all'."}

    if file:
        contents = await file.read()
        # Save or process the file as needed, e.g., save to disk or pass bytes
        run_ingestion(file_bytes=contents, chunk_type=chunk_type, page_range=parsed_range)
    else:
        run_ingestion(url=url, chunk_type=chunk_type, page_range=parsed_range)

    return {"status": "✅ Ingestion complete"}

@app.post("/ask")
def ask_question(data: QuestionRequest):
    if not data.question.strip():
        return {"error": "❌ Question cannot be empty."}
    answer = answer_question(data.question)
    return {"question": data.question, "answer": answer}
