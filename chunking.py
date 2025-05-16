# chunking.py

import nltk
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

class Chunker:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def character_chunking(self, text, chunk_size=100):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def word_chunking(self, text):
        return text.split()

    def sentence_chunking(self, text):
        return nltk.sent_tokenize(text)

    def recursive_chunking(self, text, chunk_size=200):
        if len(text) <= chunk_size:
            return [text]
        else:
            mid = len(text) // 2
            return (
                self.recursive_chunking(text[:mid], chunk_size)
                + self.recursive_chunking(text[mid:], chunk_size)
            )
    def semantic_chunking(self, text, num_chunks=5):
        sentences = self.sentence_chunking(text)

    # Safety check: reduce number of clusters if sentences are fewer
        num_sentences = len(sentences)
        if num_sentences < 2:
           return [text]  # Not enough data to cluster
        actual_clusters = min(num_chunks, num_sentences)

        embeddings = self.model.encode(sentences)
        kmeans = KMeans(n_clusters=actual_clusters, random_state=0).fit(embeddings)

        clustered_sentences = {i: [] for i in range(actual_clusters)}
        for idx, label in enumerate(kmeans.labels_):
            clustered_sentences[label].append(sentences[idx])

        chunks = [' '.join(clustered_sentences[i]) for i in range(actual_clusters)]
        return chunks



