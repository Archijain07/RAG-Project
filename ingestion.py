import os
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from chunking import Chunker
from chroma_service import ChromaHandler
from tqdm import tqdm

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ PDF successfully downloaded to: {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download PDF: {e}")
        return False

def extract_text_from_pdf_page(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list[Document]: A list of Document objects, each representing a page in the PDF.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    return documents

def apply_chunking(chunker, text, chunk_type):
    if chunk_type == "sentence":
        return chunker.sentence_chunking(text)
    elif chunk_type == "word":
        return chunker.word_chunking(text)
    elif chunk_type == "character":
        return chunker.character_chunking(text)
    elif chunk_type == "recursive":
        return chunker.recursive_chunking(text)
    elif chunk_type == "semantic":
        return chunker.semantic_chunking(text)
    else:
        print("❌ Invalid chunk type!")
        return None

def parse_page_range_input(page_input):
    try:
        parts = page_input.split("-")
        if len(parts) != 2:
            raise ValueError
        start = int(parts[0])
        end = int(parts[1])
        if start > end or start < 1:
            raise ValueError
        return (start, end)
    except ValueError:
        print("❌ Invalid page range format. Use format like 1-3.")
        return None

def run_ingestion(url, chunk_type="recursive", page_range=(1, 3)):
    filename = os.path.basename(url)
    save_path = os.path.join(".", filename)

    if not download_pdf(url, save_path):
        return

    chunker = Chunker()
    handler = ChromaHandler()
    total_docs = []
    extracted_pdf=extract_text_from_pdf_page(save_path)
    if page_range is None:
        page_nums = range(1, len(extracted_pdf) + 1)
    else:
        page_nums = range(page_range[0], page_range[1] + 1)

    if page_range is None:
         page_nums = range(1, len(extracted_pdf) + 1)
    else:
         page_nums = range(page_range[0], page_range[1] + 1)

    for page_num in tqdm(page_nums):


        print(f"\n📄 Processing Page {page_num}...")
        text = extracted_pdf[page_num-1].page_content
        if text:
            chunks = apply_chunking(chunker, text, chunk_type)
            if chunks:
                page_docs = []
                for i, chunk in enumerate(chunks):
                    print(f"\n🧩 Chunk {i+1} on Page {page_num}:\n{chunk}\n{'-'*60}")
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": filename,
                            "page": page_num,
                            "chunk_type": chunk_type
                        },
                        id=f"{page_num}-{i+1}"
                    )
                    page_docs.append(doc)
                total_docs.extend(page_docs)
                print(f"✅ Page {page_num}: {len(page_docs)} chunks.")
            else:
                print(f"⚠️ No chunks generated for page {page_num}.")
        else:
            print(f"⚠️ Could not extract text from page {page_num}.")

    if total_docs:
        handler.ingest_documents(total_docs)
        print(f"\n🎉 Ingestion Complete: {len(total_docs)} chunks from {filename} ingested to ChromaDB!")
    else:
        print("⚠️ No content was ingested.")

if __name__ == "__main__":
    url = input("🔗 Enter the URL of the PDF to download and ingest: ").strip()
    chunk_type = input("🔀 Enter chunking type (sentence, word, character, recursive, semantic): ").strip().lower()
    page_input = input("📄 Enter page range to extract (e.g., 1-3): ").strip()
    page_range = parse_page_range_input(page_input)

    if page_range:
        run_ingestion(url, chunk_type=chunk_type, page_range=page_range)


