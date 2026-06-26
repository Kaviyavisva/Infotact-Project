from iot_alert import IoTAlertHandler
from search_engine import SearchEngine


class RAGPipeline:
    """
    Integrates the IoT Alert Handler and Search Engine.
    """

    def __init__(self):
        self.alert_handler = IoTAlertHandler()
        self.search_engine = SearchEngine()

    def process_alerts(self):
        """
        Executes the RAG workflow.
        """

        alerts = self.alert_handler.generate_alerts()

        for alert in alerts:

            print("=" * 80)
            print("Machine ID :", alert["machine_id"])
            print("Error Code :", alert["error_code"])
            print("Search Query :", alert["search_query"])

            documents = self.search_engine.search_query(
                alert["search_query"]
            )

            print("\nRetrieved Chunks:\n")

            for i, doc in enumerate(documents, start=1):
                print(f"Chunk {i}:")
                print(doc)
                print("-" * 80)


if __name__ == "__main__":

    pipeline = RAGPipeline()

    pipeline.process_alerts()