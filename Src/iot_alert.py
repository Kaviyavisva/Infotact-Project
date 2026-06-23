import json

# Read chunks generated in Week 1
with open("../Output/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Error keywords to look for
keywords = [
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

alerts = []

# Process chunks
for i, chunk in enumerate(chunks):
    machine_id = f"HVAC_{i+1:03}"

    found = False

    for keyword in keywords:
        if keyword.lower() in chunk.lower():
            error_code = keyword.replace(" ", "_")

            # Create search query automatically
            query = f"How to fix {error_code} in machine {machine_id}?"

            alerts.append({
                "machine_id": machine_id,
                "error_code": error_code,
                "search_query": query
            })

            found = True
            break

# Print alerts
for alert in alerts:
    print("Machine ID :", alert["machine_id"])
    print("Error Code :", alert["error_code"])
    print("Search Query :", alert["search_query"])
    print("-" * 50)