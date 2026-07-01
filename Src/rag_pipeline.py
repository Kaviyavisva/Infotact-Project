"""
Final RAG Pipeline Integration
IoT Alert → Retrieval → Recommendation → Final Output
"""

import json
from pathlib import Path

from search_engine import search_query
from recommendation_engine import RecommendationEngine
from prompt_builder import PromptBuilder
from llm_engine import LLMEngine


class RAGPipeline:

    def __init__(self):

        self.recommendation_engine = RecommendationEngine()
        self.prompt_builder = PromptBuilder()
        self.llm_engine = LLMEngine()

        print("RAG Pipeline initialized")


    def process_alert(self, alert):

        machine_id = alert["machine_id"]
        sensor = alert["sensor"]
        value = alert["sensor_value"]
        error = alert["error_code"]
        severity = alert["severity"]


        query = (
            f"How to fix {error} "
            f"in air conditioner "
            f"with {severity} severity?"
        )


        print("\n================================")
        print("IoT ALERT")
        print("================================")

        print(f"Machine ID : {machine_id}")
        print(f"Sensor     : {sensor}")
        print(f"Value      : {value}")
        print(f"Error      : {error}")
        print(f"Severity   : {severity}")

        print("\nGenerated Query:")
        print(query)



        # Retrieval

        chunks = search_query(query)


        print("\nRetrieved Chunks:")

        for chunk in chunks:
            print(chunk[:100])


        # Recommendation

        recommendation = (
            self.recommendation_engine
            .analyze_chunks(
                chunks,
                query
            )
        )


        report = (
            self.recommendation_engine
            .format_recommendation(
                recommendation
            )
        )


        return report



if __name__ == "__main__":


    pipeline = RAGPipeline()


    # Read IoT alerts

    alert_file = Path("output/alerts.json")


    with open(alert_file,"r") as f:

        alerts = json.load(f)



    print("\nTotal IoT Alerts:",len(alerts))



    # Process first alert for demo

    final_report = pipeline.process_alert(
        alerts[0]
    )


    print("\n\n========== FINAL OUTPUT ==========")

    print(final_report)