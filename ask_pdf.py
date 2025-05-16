# ask_pdf.py

import os
from dotenv import load_dotenv  
import google.generativeai as genai
from chroma_service import ChromaHandler

# Load .env
load_dotenv()

# ✅ Set your Gemini API key (or use environment variable)
## or paste directly as a string
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer_with_gemini(question, context_chunks):
    context = "\n\n".join([f"- {chunk.page_content}" for chunk in context_chunks])
    prompt = (
        f"You are an assistant that answers questions based on a PDF document.\n\n"
        f"📄 Context:\n{context}\n\n"
        f"❓ Question: {question}\n\n"
        f"💬 Answer:"
    )

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

def answer_question(question):
    handler = ChromaHandler()
    context_chunks = handler.search_similar(question, k=5)
    return generate_answer_with_gemini(question, context_chunks)

if __name__ == "__main__":
    question = input("❓ Ask a question from the PDF: ").strip()
    if not question:
        print("⚠️ Please enter a valid question.")
    else:
        answer = answer_question(question)
        print(f"\n📘 Answer:\n{answer}")



