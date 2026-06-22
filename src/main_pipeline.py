import json
from vector_store import VectorStore

# Load chunks
with open("output/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load embeddings
with open("output/embeddings.json", "r", encoding="utf-8") as f:
    embeddings = json.load(f)

# Create Vector Store
vector_store = VectorStore()

print("Vector Store Created Successfully")
print("Chunks:", len(chunks))
print("Embeddings:", len(embeddings))
# Generate IDs
ids = [f"chunk_{i}" for i in range(len(chunks))]

print("IDs generated:", len(ids))
# Store in ChromaDB
vector_store.upsert_documents(
    ids=ids,
    documents=chunks,
    embeddings=embeddings
)

print("Documents stored successfully!")