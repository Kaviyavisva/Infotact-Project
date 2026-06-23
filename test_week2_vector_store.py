"""
Week 2 Integration Test: Vector Store Ingestion & Retrieval Workflow
This script simulates the pipeline: chunker.py -> embedder.py -> vector_store.py
"""

from vector_store import VectorStore
from vector_storage_integration import store_vectors_efficiently, retrieve_vectors

def run_integration_test():
    print("=== Week 2 Integration Test: Vector Store Pipeline ===\n")
    
    # 1. Initialize the target VectorStore using a test directory to preserve main data
    test_persist_dir = "chroma_db_week2_test"
    print(f"[*] Initializing VectorStore at '{test_persist_dir}'...")
    vs = VectorStore(collection_name="week2_integration_test", persist_directory=test_persist_dir)
    
    # 2. Simulate chunker.py output (Sample Maintenance Manuals)
    chunks = [
        "To fix a motor overheating, first check the cooling fan and clean any debris.",
        "Hydraulic pressure loss can be caused by a leaking seal in the main cylinder.",
        "If the motor overheats frequently, inspect the stator windings for short circuits.",
        "Routine maintenance requires lubricating the conveyor belt rollers every 30 days."
    ]
    
    metadatas = [
        {"manual": "Motor_Maint_v1", "section": "Troubleshooting", "page": 42},
        {"manual": "Hydraulics_v2", "section": "Diagnostics", "page": 89},
        {"manual": "Motor_Maint_v2", "section": "Electrical", "page": 12},
        {"manual": "Conveyor_v1", "section": "Routine", "page": 5}
    ]

    # 3. Simulate embedder.py output (Generating sample 3D vectors)
    # We construct mock embeddings so that the motor-related vectors match closely to our test query.
    embeddings = [
        [0.9, 0.1, 0.1],  # chunk1 (Motor issue)
        [0.1, 0.9, 0.1],  # chunk2 (Hydraulic issue)
        [0.8, 0.2, 0.1],  # chunk3 (Motor issue)
        [0.2, 0.2, 0.8],  # chunk4 (Conveyor issue)
    ]
    
    # 4. Store embeddings using the Week 2 Integration Workflow
    print("\n[*] Simulating embedder.py -> vector_store.py handoff (Batch Ingestion)...")
    ingest_stats = store_vectors_efficiently(
        vector_store=vs,
        chunks=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        batch_size=2  # use a small batch size to test batching logic
    )
    
    print(f"[+] Ingestion Status: {ingest_stats['status']}")
    print(f"[+] Items Inserted: {ingest_stats['total_inserted']} / {ingest_stats['total_attempted']}")
    print(f"[+] Execution Time: {ingest_stats['execution_time_seconds']}s")
    
    # Verify insertion worked dynamically
    assert ingest_stats['total_inserted'] == 4, "Integration Test Failed: Missing vectors."

    # 5. Retrieve vectors simulating search_engine.py
    print("\n[*] Simulating Retrieval Query: 'motor overheating fix'")
    # Mock embedding representing 'motor overheating fix' (should physically align with chunk1 and chunk3)
    query_embedding = [0.95, 0.05, 0.1]
    
    results = retrieve_vectors(
        vector_store=vs,
        query_embedding=query_embedding,
        top_k=3
    )

    # 6. Verify and Print Outputs
    print("\n=== Retrieval Results ===")
    
    # Ensure results were actually returned
    assert len(results["ids"]) > 0, "Integration Test Failed: No results retrieved."
    
    for i in range(len(results["ids"])):
        print("-" * 50)
        print(f"Result Rank : {i + 1}")
        print(f"ID          : {results['ids'][i]}")
        print(f"Distance    : {results['distances'][i]:.4f}")
        print(f"Metadata    : {results['metadatas'][i]}")
        print(f"Document    : {results['documents'][i]}")
        print("-" * 50)

    print("\n[+] Week 2 Integration Test Completed Successfully.")

if __name__ == "__main__":
    run_integration_test()
