"""
Custom exceptions for the VectorStore and RAG system.
"""

class VectorStoreError(Exception):
    """Base exception for all VectorStore-related errors."""
    pass

class InvalidEmbeddingError(VectorStoreError):
    """Raised when an embedding is invalid, empty, or improperly formatted."""
    pass

class DimensionMismatchError(VectorStoreError):
    """Raised when an embedding's dimension does not match the collection's expected dimension."""
    pass

class DuplicateIDError(VectorStoreError):
    """Raised when an attempt is made to insert a document with an ID that already exists."""
    pass

class EmptyDocumentError(VectorStoreError):
    """Raised when a document text is empty."""
    pass

class InvalidTopKError(VectorStoreError):
    """Raised when the top_k parameter for a search is invalid (e.g., <= 0)."""
    pass

class DatabaseFailureError(VectorStoreError):
    """Raised when the underlying ChromaDB instance encounters an error."""
    pass

class UnexpectedError(VectorStoreError):
    """Raised for any unexpected exceptions that occur during VectorStore operations."""
    pass
