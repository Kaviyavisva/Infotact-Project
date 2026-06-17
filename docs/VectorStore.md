# VectorStore Module Documentation

## Overview
The `VectorStore` module provides an enterprise-grade, clean architecture interface for interacting with ChromaDB within the Prescriptive Maintenance RAG Agent. It isolates vector storage logic, handles database lifecycle management, provides input validation, and manages bulk upsertions and similarity searches safely.

---

## Developer Guidelines
1. **Dependency Injection**: The `VectorStore` avoids hardcoding client initialization. Always pass a `ChromaDBClientManager` into the constructor to decouple database settings from vector operations. This makes unit testing via fixtures simple.
2. **Error Handling**: The class implements strict input validation. Always wrap operations in `try/except` locally if you anticipate malformed data in downstream ETL pipelines.
3. **Batching Execution**: The `upsert_documents` method automatically batches payloads (`batch_size=100`) to prevent overwhelming the vector database limits during bulk data imports.
4. **Logging Infrastructure**: All methods strictly integrate with `loguru`. Print statements are prohibited to ensure logging output targets persistent `.log` files cleanly.

---

## Sample Usage Example

```python
from src.rag.vectorstore import VectorStore
from src.rag.database import ChromaDBClientManager

# 1. Initialize the persistent client manager and the vector store
db_manager = ChromaDBClientManager(collection_name="maintenance_logs")
vector_store = VectorStore(db_manager=db_manager)

# 2. Upsert vectors (batched automatically)
ids = ["log-001", "log-002"]
documents = ["Engine overheating at 200C.", "Hydraulic pressure dropped below threshold."]
embeddings = [[0.1, 0.45, 0.2], [0.8, 0.12, 0.33]]
metadatas = [
    {"priority": "high", "system": "engine"}, 
    {"priority": "critical", "system": "hydraulics"}
]

# Insert or update
stats = vector_store.upsert_documents(
    ids=ids, 
    documents=documents, 
    embeddings=embeddings, 
    metadatas=metadatas
)
print("Upsert Status:", stats["status"])

# 3. Perform a Semantic Similarity Search
query_embedding = [0.15, 0.40, 0.25]
results = vector_store.search(query_embedding=query_embedding, top_k=1)

print(f"Nearest Match ID: {results['ids'][0]}")
print(f"Document Text: {results['documents'][0]}")
print(f"Metadata: {results['metadatas'][0]}")
print(f"Distance/Similarity Score: {results['distances'][0]}")
```

---

## API Documentation

### `VectorStore` Class
High-level repository for managing all vector database interactions in the application.

#### `__init__(self, db_manager: Optional[ChromaDBClientManager] = None, collection_name: str = "default_collection")`
Initializes the VectorStore instance.
* **`db_manager`**: An injected, pre-initialized manager. If `None`, a new manager is automatically instantiated.
* **`collection_name`**: The fallback collection name to target if `db_manager` is not provided.

#### `upsert_documents(self, ids: List[str], documents: List[str], embeddings: List[List[float]], metadatas: Optional[List[Dict[str, Any]]] = None, batch_size: int = 100) -> Dict[str, Any]`
Safely inserts or updates documents, embeddings, and metadata in dynamic batches.
* **`ids`**: Unique string identifiers for the data.
* **`documents`**: Plain text content of the documents.
* **`embeddings`**: The generated vector arrays matching document indices.
* **`metadatas`**: Optional dictionaries attaching properties to vectors for downstream filtering.
* **`batch_size`**: The payload size limit per network transaction (default: `100`).
* **Returns**: A dictionary with telemetry (`total_attempted`, `total_upserted`, `batches_processed`, `status`, `error`).
* **Raises**: `ValueError` immediately on empty lists, length mismatches, or invalid vector dimensionality.

#### `search(self, query_embedding: List[float], top_k: int = 3) -> Dict[str, List[Any]]`
Retrieves top _K_ nearest neighbors for a single vector.
* **`query_embedding`**: The 1D vector embedding generated from the user's prompt.
* **`top_k`**: The absolute maximum ceiling of results to retrieve (default: `3`).
* **Returns**: A flattened dictionary map isolating `"ids"`, `"documents"`, `"metadatas"`, and `"distances"`.
* **Raises**: `ValueError` if `top_k < 1` or if the input embedding is empty.

#### `check_health(self) -> bool`
Executes an active ping to the persistent storage layer heartbeat. Returns `True` if active and healthy.

#### `document_count(self) -> int`
Reads the exact count of items persisted in the active collection.

#### `reset_collection(self) -> None`
**Destructive Action**. Completely wipes all existing vectors, deletes the physical table, and recreates an empty schema shell. Used heavily in integration testing setup blocks.
