from pathlib import Path
import random
import faker
import json
import csv
import os

fake = faker.Faker()

PARAMETERS_PATH = os.getenv("CSM_PARAMETERS_ABSOLUTE_PATH")
DATASET_PATH = os.getenv("CSM_DATASET_ABSOLUTE_PATH")
params_path = Path(f"{PARAMETERS_PATH}/parameters.json")
with open(params_path, "r", encoding="utf-8") as f:
    params = json.load(f)

NUM_CUSTOMERS = int(params[0]["value"])
NUM_CONNECTIONS = NUM_CUSTOMERS * 2

customers = []
for _ in range(NUM_CUSTOMERS):
    name = fake.name()
    customers.append({
        "id": name,
        "Name": name,
        "Satisfaction": 0,
        "SurroundingSatisfaction": 0,
        "Thirsty": False
    })

with open(f"{DATASET_PATH}/Customer.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","Name", "Satisfaction", "SurroundingSatisfaction", "Thirsty"])
    writer.writeheader()
    writer.writerows(customers)

connections = []
for _ in range(NUM_CONNECTIONS):
    c1, c2 = random.sample(customers, 2)
    connections.append({"id":c1["Name"]+c2["Name"], "src": c1["Name"], "dest": c2["Name"]})

with open(f"{DATASET_PATH}/arc_to_Customer.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","src", "dest"])
    writer.writeheader()
    writer.writerows(connections)

bar_data = [{"id": "MyBar", "NbWaiters": 15, "RestockQty": 40, "Stock": 50}]
with open(f"{DATASET_PATH}/Bar.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=bar_data[0].keys())
    writer.writeheader()
    writer.writerows(bar_data)

print("customers.csv, connections.csv and bar.csv generated successfully!")