"""
IoT Alert Generator Module
Generates machine fault alerts and creates search queries
for the Prescriptive Maintenance RAG Pipeline.

Workflow:
IoT Alert
    ↓
Search Query
    ↓
RAG Pipeline
"""

import json
import random
import os
from datetime import datetime


# ----------------------------
# Project Paths
# ----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

ALERT_FILE = os.path.join(
    OUTPUT_DIR,
    "alerts.json"
)


# ----------------------------
# IoT Alert Templates
# ----------------------------

alert_templates = [

    {
        "sensor": "Temperature Sensor",
        "error_code": "OVERHEATING",
        "severity": "HIGH",
        "value_range": (85, 110),
        "unit": "C"
    },

    {
        "sensor": "Pressure Sensor",
        "error_code": "REFRIGERANT_LEAK",
        "severity": "MEDIUM",
        "value_range": (20, 35),
        "unit": "psi"
    },

    {
        "sensor": "Current Sensor",
        "error_code": "ELECTRICAL_OVERLOAD",
        "severity": "HIGH",
        "value_range": (15, 30),
        "unit": "A"
    },

    {
        "sensor": "Voltage Sensor",
        "error_code": "SHORT_CIRCUIT",
        "severity": "HIGH",
        "value_range": (180, 260),
        "unit": "V"
    },

    {
        "sensor": "Vibration Sensor",
        "error_code": "ABNORMAL_VIBRATION",
        "severity": "MEDIUM",
        "value_range": (10, 40),
        "unit": "mm/s"
    }

]


# ----------------------------
# Generate IoT Alerts
# ----------------------------

def generate_alerts():

    NUM_MACHINES = 25

    FAULT_PROBABILITY = 0.70


    alerts = []


    for i in range(NUM_MACHINES):

        machine_id = f"HVAC_{i+1:03}"


        # healthy machine
        if random.random() > FAULT_PROBABILITY:
            continue


        fault_count = random.randint(1,2)


        selected_faults = random.sample(
            alert_templates,
            k=fault_count
        )


        for fault in selected_faults:


            value = random.randint(
                fault["value_range"][0],
                fault["value_range"][1]
            )


            alert = {


                "machine_id": machine_id,


                "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),


                "sensor":
                fault["sensor"],


                "sensor_value":
                f"{value} {fault['unit']}",


                "error_code":
                fault["error_code"],


                "severity":
                fault["severity"]

            }


            alerts.append(alert)


    return alerts



# ----------------------------
# Save Alerts
# ----------------------------

def save_alerts(alerts):


    with open(
        ALERT_FILE,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            alerts,
            file,
            indent=4
        )



# ----------------------------
# Load Alerts
# ----------------------------

def load_alerts():


    with open(
        ALERT_FILE,
        "r",
        encoding="utf-8"
    ) as file:


        return json.load(file)



# ----------------------------
# Convert IoT Alert to Search Query
# ----------------------------

def create_search_query(alert):


    query = (

        f"How to fix "
        f"{alert['error_code']} "

        f"in air conditioner "

        f"with "
        f"{alert['severity']} severity?"

    )


    return query



# ----------------------------
# Main Execution
# ----------------------------


if __name__ == "__main__":


    alerts = generate_alerts()


    print("\n========== SUMMARY ==========")

    print(
        f"Total Alerts: {len(alerts)}"
    )


    save_alerts(alerts)


    print(
        "\nalerts.json generated successfully."
    )


    alerts = load_alerts()



    print(
        "\n========== IoT ALERTS ==========\n"
    )


    for alert in alerts:


        print(
            "Machine ID   :",
            alert["machine_id"]
        )


        print(
            "Sensor       :",
            alert["sensor"]
        )


        print(
            "Value        :",
            alert["sensor_value"]
        )


        print(
            "Error Code   :",
            alert["error_code"]
        )


        print(
            "Severity     :",
            alert["severity"]
        )


        print(
            "Search Query :",
            create_search_query(alert)
        )


        print("-"*60)



    print(
        "\nAll alerts processed successfully."
    )