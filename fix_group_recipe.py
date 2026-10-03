import dataikuapi
import json
import os
from dotenv import load_dotenv

load_dotenv()

DSS_URL = os.environ["DSS_URL"]
API_KEY = os.environ["DSS_API_KEY"]
PROJECT_KEY = "ANALYTICAL_READY_DATASETS"

client = dataikuapi.DSSClient(DSS_URL, API_KEY)
project = client.get_project(PROJECT_KEY)

print("Fixing group_rx_by_drug recipe...")
recipe = project.get_recipe("group_rx_by_drug")
settings = recipe.get_settings()
payload = settings.get_json_payload()

# Set group-by keys: DRUG_NAME, SPECIALTY
payload["keys"] = [
    {"column": "DRUG_NAME", "type": "value"},
    {"column": "SPECIALTY", "type": "value"}
]

# Update values: enable countDistinct on PATIENT_ID and count on RX_ID
for v in payload["values"]:
    if v["column"] == "PATIENT_ID":
        v["countDistinct"] = True
    elif v["column"] == "RX_ID":
        v["count"] = True

# Disable the global count since we have specific aggregations
payload["globalCount"] = False

settings.set_json_payload(payload)
settings.save()
print("  -> Keys: DRUG_NAME, SPECIALTY")
print("  -> Aggregations: countDistinct(PATIENT_ID), count(RX_ID)")
print("Done!")
