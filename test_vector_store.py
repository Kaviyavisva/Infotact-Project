"""
Simple test script to verify VectorStore functionality for Week 1.
"""

from vector_store import VectorStore

def run_test():
    print("Initializing VectorStore...")
    # Initialize with a test directory to avoid polluting main data
    vs = VectorStore(collection_name="test_maintenance_docs", persist_directory="chroma_db_test")

    print("\nInserting sample maintenance manual chunks...")
    ids = ["chunk1", "chunk2", "chunk3", "chunk4"]
    documents = [
        "To fix a motor overheating, first check the cooling fan and clean any debris.",
        "Hydraulic pressure loss can be caused by a leaking seal in the main cylinder.",
        "If the motor overheats frequently, inspect the stator windings for short circuits.",
        "Routine maintenance requires lubricating the conveyor belt rollers every 30 days."
    ]
    
    # Mock embeddings for demonstration purposes (simulating 3-dimensional vectors)
    # chunk1 and chunk3 are given vectors closer to the "motor overheating" query
    embeddings = [
        [0.9, 0.1, 0.1],  # chunk1 (Motor issue)
        [0.1, 0.9, 0.1],  # chunk2 (Hydraulic issue)
        [0.8, 0.2, 0.1],  # chunk3 (Motor issue)
        [0.2, 0.2, 0.8],  # chunk4 (Conveyor issue)
    ]
    
    metadatas = [
        {"source": "manual_v1", "page": 42},
        {"source": "manual_v1", "page": 89},
        {"source": "manual_v2", "page": 12},
        {"source": "manual_v1", "page": 5}
    ]

    # Insert data
    vs.upsert_documents(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
    print("Insertion complete.")

    print("\nSearching for 'motor overheating fix'...")
    # Mock query embedding simulating the query "motor overheating fix"
    query_embedding = [0.95, 0.05, 0.1]
    
    # Search top 3
    results = vs.search(query_embedding=query_embedding, top_k=3)

    print(f"\nTop {len(results['ids'])} Retrieved Chunks:")
    print("-" * 40)
    for i in range(len(results['ids'])):
        print(f"Result {i + 1}")
        print(f"ID       : {results['ids'][i]}")
        print(f"Distance : {results['distances'][i]:.4f}")
        print(f"Metadata : {results['metadatas'][i]}")
        print(f"Document : {results['documents'][i]}")
        print("-" * 40)

if __name__ == "__main__":
    run_test()
