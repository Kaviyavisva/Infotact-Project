import json
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read chunks.json
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract text
texts = chunks

# Generate embeddings
embeddings = model.encode(texts)

# Convert numpy array to list
embeddings = embeddings.tolist()

# Save embeddings
with open("embeddings.json", "w", encoding="utf-8") as f:
    json.dump(embeddings, f)

print("Embeddings generated successfully!")
