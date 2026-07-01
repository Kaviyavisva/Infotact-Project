import json
import random
from datetime import datetime

# ----------------------------
# Sample IoT Alert Templates
# ----------------------------
alert_templates = [
    {
        "sensor": "Temperature Sensor",
        "error_code": "OVERHEATING",
        "severity": "HIGH",
        "value_range": (85, 110),
        "unit": "°C"
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
    },
    {
        "sensor": "Smoke Sensor",
        "error_code": "FIRE_DETECTED",
        "severity": "HIGH",
        "value_range": (1, 10),
        "unit": "ppm"
    }
]

# ------------------------------------
# Generate Realistic IoT Alerts
# ------------------------------------

NUM_MACHINES = 25        # Total machines monitored
FAULT_PROBABILITY = 0.70 # 70% chance a machine has a fault

alerts = []

healthy_machines = 0

for i in range(NUM_MACHINES):

    machine_id = f"HVAC_{i+1:03}"

    # Some machines are healthy
    if random.random() > FAULT_PROBABILITY:
        healthy_machines += 1
        continue

    # A machine can have 1 or 2 faults
    number_of_faults = random.randint(1, 2)

    selected_templates = random.sample(
        alert_templates,
        k=min(number_of_faults, len(alert_templates))
    )

    for template in selected_templates:

        value = random.randint(
            template["value_range"][0],
            template["value_range"][1]
        )

        alert = {
            "machine_id": machine_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sensor": template["sensor"],
            "sensor_value": f"{value} {template['unit']}",
            "error_code": template["error_code"],
            "severity": template["severity"]
        }

        alerts.append(alert)

print("\n========== SUMMARY ==========")
print(f"Machines Monitored : {NUM_MACHINES}")
print(f"Healthy Machines   : {healthy_machines}")
print(f"Faulty Machines    : {NUM_MACHINES - healthy_machines}")
print(f"Total Alerts       : {len(alerts)}")

# Save Alerts
with open("../Output/alerts.json", "w", encoding="utf-8") as f:
    json.dump(alerts, f, indent=4)

print("alerts.json generated successfully.\n")

# ------------------------------------
# Read Alerts
# ------------------------------------

with open("../Output/alerts.json", "r", encoding="utf-8") as f:
    alerts = json.load(f)

# ------------------------------------
# Process Alerts
# ------------------------------------

print("========== IoT ALERTS ==========\n")

for alert in alerts:

    machine_id = alert["machine_id"]
    error_code = alert["error_code"]
    severity = alert["severity"]

    search_query = (
        f"How to fix {error_code} "
        f"in machine {machine_id} "
        f"with {severity} severity?"
    )

    print(f"Machine ID   : {machine_id}")
    print(f"Sensor       : {alert['sensor']}")
    print(f"Sensor Value : {alert['sensor_value']}")
    print(f"Error Code   : {error_code}")
    print(f"Severity     : {severity}")
    print(f"Search Query : {search_query}")
    print("-" * 60)

    # Integration point
    # from search_engine import search_documents
    # result = search_documents(search_query)

print("\nAll alerts processed successfully.")