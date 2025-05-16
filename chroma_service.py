from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class ChromaHandler:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=embeddings,
            persist_directory="./chroma_langchain_db"
        )

    def ingest_documents(self, documents):
        self.vector_store.add_documents(documents)

    def search_similar(self, query, k=3):
        return self.vector_store.similarity_search(query, k=k)
