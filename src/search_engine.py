import chromadb

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Open collection
collection = client.get_collection("manual_chunks")

def search_query(query):

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return results["documents"][0]