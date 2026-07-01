import chromadb
from sentence_transformers import SentenceTransformer

# STEP 3: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Open collection
collection = client.get_collection("manual_chunks")

def search_query(query):

    # Handle empty query
    if not query.strip():
        return ["Please enter a valid query."]

    # Generate query embedding
    query_embedding = model.encode(query).tolist()

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Return top 3 chunks
    return results["documents"][0]
