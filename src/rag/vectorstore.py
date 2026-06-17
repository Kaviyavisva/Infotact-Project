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
