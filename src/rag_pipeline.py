from iot_alert import IoTAlertHandler
from search_engine import SearchEngine
from recommendation_engine import RecommendationEngine


class RAGPipeline:
    """
    Integrates the IoT Alert Handler, Search Engine,
    and Recommendation Engine.
    """

    def __init__(self):
        self.alert_handler = IoTAlertHandler()
        self.search_engine = SearchEngine()
        self.recommendation_engine = RecommendationEngine()

    def process_alerts(self):
        """
        Executes the complete Week 3 RAG workflow.
        """

        alerts = self.alert_handler.generate_alerts()

        if not alerts:
            print("No alerts found.")
            return

        # Process only the first alert
        alert = alerts[0]

        print("=" * 80)
        print("Machine ID :", alert["machine_id"])
        print("Error Code :", alert["error_code"])
        print("Search Query :", alert["search_query"])

        # Retrieve relevant chunks
        documents = self.search_engine.search_query(
            alert["search_query"]
        )

        # Generate recommendation
        recommendation = self.recommendation_engine.analyze_chunks(
            retrieved_chunks=documents,
            alert_context=alert["search_query"]
        )

        # Format recommendation
        report = self.recommendation_engine.format_recommendation(
            recommendation
        )

        print("\n")
        print(report)
        print("\n")


if __name__ == "__main__":

    pipeline = RAGPipeline()

    pipeline.process_alerts()