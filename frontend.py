import streamlit as st
import requests

# API base URL (adjust if deployed elsewhere)
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PDF QA App", layout="centered")

st.title("📄 PDF Question Answering")
st.write("Ingest a PDF and ask questions from it using a semantic search + LLM pipeline.")

# --- Ingestion Section ---
# --- Ingestion Section ---
st.subheader("Step 1: Ingest a PDF")

with st.form("ingest_form"):
    url = st.text_input("Enter PDF URL", placeholder="https://example.com/sample.pdf")
    chunk_type = st.selectbox("Select Chunking Method", ["recursive", "sentence", "word", "character"])

    all_pages = st.checkbox("Ingest entire PDF?")
    page_range = None
    if not all_pages:
        page_range = st.text_input("Page Range (e.g. 1-3)", value="1-3")

    ingest_button = st.form_submit_button("📥 Ingest PDF")

    if ingest_button:
        with st.spinner("Ingesting PDF..."):
            response = requests.post(f"{API_URL}/ingest", json={
                "url": url,
                "chunk_type": chunk_type,
                "page_range": page_range if page_range else "all"
            })
            if response.status_code == 200 and "status" in response.json():
                st.success(response.json()["status"])
            else:
                st.error(response.json().get("error", "Unknown error during ingestion."))


# --- QA Section ---
st.subheader("Step 2: Ask a Question")

question = st.text_input("Enter your question", placeholder="What is the main topic discussed?")
if st.button("🔍 Ask"):
    if question.strip():
        with st.spinner("Getting answer from LLM..."):
            response = requests.post(f"{API_URL}/ask", json={"question": question})
            if response.status_code == 200:
                st.markdown(f"**Answer:** {response.json().get('answer', 'No answer received.')}")
            else:
                st.error(response.json().get("error", "Failed to retrieve answer."))
    else:
        st.warning("Please enter a valid question.")
