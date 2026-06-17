"""
Vector Store module for managing Generative AI RAG operations.
"""

from typing import Optional, Dict, Any
from loguru import logger
from chromadb.api.models.Collection import Collection

# Internal dependencies
from src.rag.database import ChromaDBClientManager


class VectorStore:
    """
    High-level repository for vector database interactions in a RAG system.

    This class provides a clean, domain-specific interface to the underlying
    ChromaDB storage engine. It strictly delegates database connection and
    lifecycle management to the injected ChromaDBClientManager, adhering to
    the Single Responsibility Principle and Clean Architecture.
    """

    def __init__(self, db_manager: Optional[ChromaDBClientManager] = None, collection_name: str = "default_collection") -> None:
        """
        Initializes the VectorStore instance.

        Args:
            db_manager (Optional[ChromaDBClientManager]): An injected, pre-initialized
                manager. If None, a new ChromaDBClientManager will be instantiated.
            collection_name (str): The name of the collection to manage. Used
                only if db_manager is not provided.
        """
        logger.info("Initializing VectorStore repository...")
        
        # Dependency Injection of the database manager
        if db_manager is None:
            logger.debug(f"Instantiating default ChromaDBClientManager for collection: '{collection_name}'")
            self._db_manager = ChromaDBClientManager(collection_name=collection_name)
        else:
            logger.debug("Using injected ChromaDBClientManager instance.")
            self._db_manager = db_manager

    @property
    def collection(self) -> Collection:
        """
        Retrieves the underlying ChromaDB collection.

        Returns:
            Collection: The active ChromaDB collection instance.
        """
        return self._db_manager.collection

    def check_health(self) -> bool:
        """
        Helper method to verify database connectivity.

        Returns:
            bool: True if the database heartbeat responds, False otherwise.
        """
        try:
            heartbeat = self._db_manager.client.heartbeat()
            logger.debug(f"Vector database health check passed. Heartbeat timestamp: {heartbeat}")
            return True
        except Exception as e:
            logger.error(f"Vector database health check failed: {e}")
            return False

    def document_count(self) -> int:
        """
        Helper method to count the total number of items in the current collection.

        Returns:
            int: Total document count.
        """
        try:
            count = self.collection.count()
            logger.info(f"Retrieved document count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error fetching document count: {e}")
            raise

    def get_collection_metadata(self) -> Dict[str, Any]:
        """
        Helper method to retrieve metadata about the collection.

        Returns:
            Dict[str, Any]: Dictionary containing collection configuration and stats.
        """
        try:
            col = self.collection
            return {
                "id": str(col.id),
                "name": col.name,
                "metadata": col.metadata,
                "count": col.count(),
                "tenant": col.tenant,
                "database": col.database
            }
        except Exception as e:
            logger.error(f"Error retrieving collection metadata: {e}")
            raise

    def reset_collection(self) -> None:
        """
        Helper method to completely clear and recreate the collection.
        
        Warning: This permanently deletes all embedded documents in the collection.
        """
        collection_name = self._db_manager.collection_name
        logger.warning(f"Initiating destructive reset for collection: '{collection_name}'")
        
        try:
            # Delete the collection from the client
            self._db_manager.client.delete_collection(name=collection_name)
            logger.info(f"Collection '{collection_name}' deleted.")
            
            # Re-initialize the manager to recreate the empty collection
            self._db_manager._initialize_db()
            logger.success(f"Collection '{collection_name}' successfully reset and recreated.")
        except Exception as e:
            logger.error(f"Failed to reset collection '{collection_name}': {e}")
            raise
    def upsert_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Upserts documents, embeddings, and metadata into the vector store in batches.

        This method validates the input data, ensures uniform lengths and embedding dimensions,
        and safely upserts the data into ChromaDB. Existing IDs will be updated.

        Args:
            ids (List[str]): Unique identifiers for the documents.
            documents (List[str]): The text content of the documents.
            embeddings (List[List[float]]): The vector embeddings for the documents.
            metadatas (Optional[List[Dict[str, Any]]]): Optional metadata dictionaries for each document.
            batch_size (int): The number of documents to upsert per batch. Defaults to 100.

        Returns:
            Dict[str, Any]: Insertion statistics including attempted counts, success counts,
                and status.

        Raises:
            ValueError: If input validation fails (e.g., mismatched lengths, empty lists).
        """
        logger.info(f"Starting upsert process for {len(ids)} documents.")

        # 1. Validate Non-Empty
        if not ids or not documents or not embeddings:
            error_msg = "IDs, documents, and embeddings lists cannot be empty."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # 2. Validate Equal Lengths
        n_docs = len(ids)
        if len(documents) != n_docs or len(embeddings) != n_docs:
            error_msg = f"Mismatched lengths: {len(ids)} ids, {len(documents)} docs, {len(embeddings)} embeddings."
            logger.error(error_msg)
            raise ValueError(error_msg)

        if metadatas is not None and len(metadatas) != n_docs:
            error_msg = f"Mismatched lengths: {len(ids)} ids, {len(metadatas)} metadatas."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # 3. Validate Embedding Dimensions
        expected_dim = len(embeddings[0])
        for i, emb in enumerate(embeddings):
            if len(emb) != expected_dim:
                error_msg = f"Inconsistent embedding dimension at index {i}. Expected {expected_dim}, got {len(emb)}."
                logger.error(error_msg)
                raise ValueError(error_msg)

        # 4. Validate Metadata Format
        if metadatas is not None:
            for i, meta in enumerate(metadatas):
                if not isinstance(meta, dict):
                    error_msg = f"Invalid metadata format at index {i}. Expected dict, got {type(meta)}."
                    logger.error(error_msg)
                    raise ValueError(error_msg)

        # Prepare statistics
        stats = {
            "total_attempted": n_docs,
            "total_upserted": 0,
            "batches_processed": 0,
            "status": "success",
            "error": None
        }

        # 5. Batch Upsertion
        try:
            for i in range(0, n_docs, batch_size):
                batch_ids = ids[i:i + batch_size]
                batch_docs = documents[i:i + batch_size]
                batch_embs = embeddings[i:i + batch_size]
                batch_metas = metadatas[i:i + batch_size] if metadatas is not None else None

                # .upsert() inherently creates new records or updates existing IDs
                self.collection.upsert(
                    ids=batch_ids,
                    documents=batch_docs,
                    embeddings=batch_embs,
                    metadatas=batch_metas
                )

                stats["total_upserted"] += len(batch_ids)
                stats["batches_processed"] += 1
                logger.info(f"Successfully upserted batch {stats['batches_processed']} ({len(batch_ids)} documents).")

            logger.success(f"Upsert complete. {stats['total_upserted']}/{stats['total_attempted']} documents inserted.")

        except Exception as e:
            error_msg = f"Failed during batch upsertion at batch {stats['batches_processed'] + 1}: {str(e)}"
            logger.error(error_msg)
            stats["status"] = "partial_success" if stats["total_upserted"] > 0 else "failure"
            stats["error"] = error_msg

        return stats
