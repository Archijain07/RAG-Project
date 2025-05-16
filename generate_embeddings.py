from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Input text
text = input("Enter text to embed: ")

# Generate embedding
embedding_vector = model.encode(text)

# Print the result
print("\nEmbedding Vector:\n")
print(embedding_vector)
