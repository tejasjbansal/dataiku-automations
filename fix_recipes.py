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

# Fix Recipe 1: join_patients_prescriptions
print("Fixing join_patients_prescriptions...")
recipe1 = project.get_recipe("join_patients_prescriptions")
settings1 = recipe1.get_settings()
payload1 = settings1.get_json_payload()
payload1["joins"][0]["on"] = [{
    "column1": {"name": "PATIENT_ID", "table": 0},
    "column2": {"name": "PATIENT_ID", "table": 1},
    "type": "EQ"
}]
settings1.set_json_payload(payload1)
settings1.save()
print("  -> Fixed: JOIN ON PATIENT_ID")

# Fix Recipe 2: join_with_doctors
print("Fixing join_with_doctors...")
recipe2 = project.get_recipe("join_with_doctors")
settings2 = recipe2.get_settings()
payload2 = settings2.get_json_payload()
payload2["joins"][0]["on"] = [{
    "column1": {"name": "DOCTOR_ID", "table": 0},
    "column2": {"name": "DOCTOR_ID", "table": 1},
    "type": "EQ"
}]
settings2.set_json_payload(payload2)
settings2.save()
print("  -> Fixed: JOIN ON DOCTOR_ID")

print("\nDone! Both join recipes have proper join conditions now.")
