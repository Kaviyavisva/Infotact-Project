"""
Vector Store module for the Prescriptive Maintenance RAG Agent.
Handles storage and retrieval of document chunks using ChromaDB.
"""

from typing import List, Dict, Any, Optional
import chromadb


class VectorStore:
    """
    Manages interactions with ChromaDB for storing and searching document embeddings.
    """

    def __init__(self, collection_name: str = "maintenance_docs", persist_directory: str = "chroma_db") -> None:
        """
        Initializes the persistent ChromaDB client and loads or creates the collection.

        Args:
            collection_name (str): The name of the collection to manage.
            persist_directory (str): The local directory to store the database files.
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize the persistent client pointing to the local directory
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Automatically get or create the collection
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def upsert_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Upserts documents, embeddings, and optionally metadata into the vector store.
        Existing IDs will be updated.

        Args:
            ids (List[str]): Unique string identifiers for each document chunk.
            documents (List[str]): The actual text chunks.
            embeddings (List[List[float]]): The vector embeddings for the chunks.
            metadatas (Optional[List[Dict[str, Any]]]): Optional metadata dictionaries.

        Raises:
            ValueError: If inputs are empty or have mismatched lengths.
        """
        # Validate that inputs are not empty
        if not ids or not documents or not embeddings:
            raise ValueError("IDs, documents, and embeddings cannot be empty.")

        # Validate that lengths are equal
        n_items = len(ids)
        if len(documents) != n_items or len(embeddings) != n_items:
            raise ValueError("The lengths of ids, documents, and embeddings must be equal.")

        if metadatas is not None and len(metadatas) != n_items:
            raise ValueError("The length of metadatas must match the number of ids.")

        # Store vectors in ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> Dict[str, List[Any]]:
        """
        Searches the vector store for the top_k most similar chunks using a query embedding.

        Args:
            query_embedding (List[float]): The vector embedding of the search query.
            top_k (int): The maximum number of results to return. Defaults to 3.

        Returns:
            Dict[str, List[Any]]: A dictionary containing flat lists of retrieved data:
                - ids
                - documents
                - metadatas
                - distances
        """
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer.")

        # Perform similarity search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        # Flatten the results for a single query response
        return {
            "ids": results.get("ids", [[]])[0],
            "documents": results.get("documents", [[]])[0] if results.get("documents") else [],
            "metadatas": results.get("metadatas", [[]])[0] if results.get("metadatas") else [],
            "distances": results.get("distances", [[]])[0] if results.get("distances") else []
        }
