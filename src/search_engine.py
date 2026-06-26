import chromadb
from sentence_transformers import SentenceTransformer


class SearchEngine:
    """
    Handles query embedding and document retrieval from ChromaDB.
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.client.get_collection("maintenance_docs")

    def search_query(self, query):
        """
        Searches the vector database and returns the top 3 relevant chunks.
        """

        if not query or not query.strip():
            return []

        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        return results["documents"][0]


if __name__ == "__main__":

    engine = SearchEngine()

    query = input("Enter search query: ")

    documents = engine.search_query(query)

    print("\nTop Retrieved Chunks:\n")

    for i, doc in enumerate(documents, start=1):
        print(f"Chunk {i}:")
        print(doc)
        print("-" * 80)