# PDF Chunking App

This project allows you to process PDF documents and interact with them via a backend API and a Streamlit frontend.

## Setup Instructions

1. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the backend API (FastAPI with Uvicorn):**
   ```sh
   uvicorn app:app --reload
   ```

4. **Run the frontend (Streamlit):**
   Open a new terminal (with the virtual environment activated) and run:
   ```sh
   streamlit run frontend.py
   ```

---

Make sure to configure any required environment variables or API keys as needed.