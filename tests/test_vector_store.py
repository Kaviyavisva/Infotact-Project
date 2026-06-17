"""
Unit tests for the VectorStore module using pytest.
"""

import pytest
from typing import Dict, Any, List

from src.rag.vectorstore import VectorStore
from src.rag.database import ChromaDBClientManager


@pytest.fixture
def temp_db_manager(monkeypatch, tmp_path):
    """
    Fixture to create a temporary ChromaDB Client Manager for testing.
    Mocks the settings.CHROMA_DB_DIR to isolate tests in a temporary directory.
    """
    import config
    monkeypatch.setattr(config.settings, "CHROMA_DB_DIR", tmp_path / "chroma_db_test")
    
    manager = ChromaDBClientManager(collection_name="test_collection")
    yield manager
    
    # Teardown: clear the collection to ensure no state leaks
    try:
        manager.client.delete_collection("test_collection")
    except Exception:
        pass


@pytest.fixture
def vector_store(temp_db_manager):
    """
    Fixture to provide a clean VectorStore instance injected with a temporary DB manager.
    """
    vs = VectorStore(db_manager=temp_db_manager)
    return vs


# --- Test Cases ---

def test_initialization(vector_store):
    """Test successful initialization and database connection health."""
    assert vector_store.check_health() is True
    assert vector_store.document_count() == 0


def test_empty_database_search(vector_store):
    """Test searching an empty database returns empty results gracefully without errors."""
    results = vector_store.search(query_embedding=[0.1, 0.2, 0.3], top_k=3)
    
    assert len(results["ids"]) == 0
    assert len(results["documents"]) == 0
    assert len(results["metadatas"]) == 0
    assert len(results["distances"]) == 0


def test_upsert_valid_documents(vector_store):
    """Test standard upsert operation with valid documents, embeddings, and metadata."""
    ids = ["doc1", "doc2"]
    docs = ["Maintenance manual A", "Maintenance manual B"]
    embs = [[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]]
    metas = [{"source": "A"}, {"source": "B"}]
    
    stats = vector_store.upsert_documents(ids, docs, embs, metadatas=metas)
    
    assert stats["status"] == "success"
    assert stats["total_attempted"] == 2
    assert stats["total_upserted"] == 2
    assert vector_store.document_count() == 2


def test_upsert_duplicate_ids(vector_store):
    """Test that upserting with existing IDs updates the documents without failing."""
    ids = ["doc1"]
    docs = ["Original content"]
    embs = [[0.1, 0.1, 0.1]]
    
    # First insert
    vector_store.upsert_documents(ids, docs, embs)
    assert vector_store.document_count() == 1
    
    # Upsert duplicate ID with updated content
    new_docs = ["Updated content"]
    vector_store.upsert_documents(ids, new_docs, embs)
    
    # Count should remain 1, content should be updated
    assert vector_store.document_count() == 1
    results = vector_store.search(query_embedding=[0.1, 0.1, 0.1], top_k=1)
    assert results["documents"][0] == "Updated content"


def test_invalid_input_empty_lists(vector_store):
    """Test upsert validation raises ValueError for empty inputs."""
    with pytest.raises(ValueError, match="cannot be empty"):
        vector_store.upsert_documents([], [], [])


def test_invalid_input_mismatched_lengths(vector_store):
    """Test upsert validation raises ValueError for mismatched input list lengths."""
    with pytest.raises(ValueError, match="Mismatched lengths"):
        vector_store.upsert_documents(["id1", "id2"], ["doc1"], [[0.1], [0.2]])


def test_invalid_input_dimension_mismatch(vector_store):
    """Test upsert validation raises ValueError for inconsistent embedding dimensions."""
    ids = ["id1", "id2"]
    docs = ["doc1", "doc2"]
    embs = [[0.1, 0.2], [0.1]] # mismatched inner dimensions
    
    with pytest.raises(ValueError, match="Inconsistent embedding dimension"):
        vector_store.upsert_documents(ids, docs, embs)


def test_search_functionality(vector_store):
    """Test semantic search returns correctly ordered results based on distance."""
    ids = ["doc1", "doc2", "doc3"]
    docs = ["Engine fail", "Tire pressure low", "Engine oil leak"]
    embs = [[0.9, 0.1], [0.1, 0.9], [0.8, 0.2]]
    metas = [{"type": "engine"}, {"type": "tire"}, {"type": "engine"}]
    
    vector_store.upsert_documents(ids, docs, embs, metadatas=metas)
    
    # Query vector very close to the first and third engine items
    results = vector_store.search(query_embedding=[1.0, 0.0], top_k=2)
    
    assert len(results["ids"]) == 2
    assert "doc1" in results["ids"]
    assert "doc3" in results["ids"]
    assert "doc2" not in results["ids"]  # The tire issue should be excluded


def test_search_invalid_top_k(vector_store):
    """Test search validation correctly raises errors for an invalid top_k parameter."""
    with pytest.raises(ValueError, match="Invalid top_k"):
        vector_store.search(query_embedding=[0.1, 0.2], top_k=0)


def test_metadata_retrieval(vector_store):
    """Test that metadata is correctly preserved, attached to vectors, and retrieved."""
    ids = ["m1"]
    docs = ["content"]
    embs = [[1.0]]
    metas = [{"author": "John Doe", "priority": 5}]
    
    vector_store.upsert_documents(ids, docs, embs, metadatas=metas)
    
    results = vector_store.search(query_embedding=[1.0], top_k=1)
    
    assert len(results["metadatas"]) == 1
    retrieved_meta = results["metadatas"][0]
    assert retrieved_meta["author"] == "John Doe"
    assert retrieved_meta["priority"] == 5
