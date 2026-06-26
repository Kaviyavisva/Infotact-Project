import json


class IoTAlertHandler:
    def __init__(self):
        self.keywords = [
            "REFRIGERANT",
            "LEAK",
            "ELECTRIC SHOCK",
            "FIRE",
            "OVERHEATING",
            "SHORT CIRCUIT",
            "BURST",
            "BURN",
            "INJURY"
        ]

    def generate_alerts(self):
        """
        Reads chunks and generates IoT alerts.
        Returns a list of alerts.
        """

        with open("output/chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

        alerts = []

        for i, chunk in enumerate(chunks):
            machine_id = f"HVAC_{i+1:03}"

            for keyword in self.keywords:
                if keyword.lower() in chunk.lower():

                    error_code = keyword.replace(" ", "_")

                    query = f"How to fix {error_code} in machine {machine_id}?"

                    alerts.append({
                        "machine_id": machine_id,
                        "error_code": error_code,
                        "search_query": query
                    })

                    break

        return alerts


if __name__ == "__main__":

    handler = IoTAlertHandler()

    alerts = handler.generate_alerts()

    for alert in alerts:
        print("Machine ID :", alert["machine_id"])
        print("Error Code :", alert["error_code"])
        print("Search Query :", alert["search_query"])
        print("-" * 50)