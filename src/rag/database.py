"""
ChromaDB client initialization and collection management.
"""

from typing import Optional
import chromadb
from chromadb.api.models.Collection import Collection
from loguru import logger

# Using the centralized settings from config.py
from config import settings


class ChromaDBClientManager:
    """
    Manages the persistent connection to ChromaDB.

    This class handles the initialization of the persistent client and
    safely gets or creates collections. It acts as an underlying service
    for higher-level VectorStore classes.
    """

    def __init__(self, collection_name: str) -> None:
        """
        Initializes the ChromaDB persistent client manager.

        Args:
            collection_name (str): The name of the collection to manage.
        """
        self.collection_name = collection_name
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection: Optional[Collection] = None
        
        self._initialize_db()

    def _initialize_db(self) -> None:
        """
        Initializes the persistent ChromaDB client and the target collection.

        Raises:
            RuntimeError: If initialization fails due to permissions, corrupted
                data, or other underlying issues.
        """
        db_path = str(settings.CHROMA_DB_DIR)
        
        try:
            logger.info(f"Initializing PersistentClient at directory: {db_path}")
            self._client = chromadb.PersistentClient(path=db_path)
            
            logger.info(f"Accessing or creating collection: '{self.collection_name}'")
            self._collection = self._client.get_or_create_collection(
                name=self.collection_name
            )
            
            logger.success(f"Successfully initialized ChromaDB collection '{self.collection_name}'.")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB collection '{self.collection_name}'. Error: {e}")
            raise RuntimeError(f"ChromaDB initialization failed: {e}") from e

    @property
    def collection(self) -> Collection:
        """
        Provides access to the initialized ChromaDB collection.

        Returns:
            Collection: The active ChromaDB collection instance.

        Raises:
            RuntimeError: If accessed before the collection is successfully initialized.
        """
        if self._collection is None:
            logger.error("ChromaDB collection accessed prior to successful initialization.")
            raise RuntimeError("ChromaDB collection is not initialized.")
        return self._collection

    @property
    def client(self) -> chromadb.PersistentClient:
        """
        Provides access to the underlying persistent client.

        Returns:
            chromadb.PersistentClient: The ChromaDB persistent client instance.
            
        Raises:
            RuntimeError: If accessed before the client is successfully initialized.
        """
        if self._client is None:
            logger.error("ChromaDB client accessed prior to successful initialization.")
            raise RuntimeError("ChromaDB client is not initialized.")
        return self._client
