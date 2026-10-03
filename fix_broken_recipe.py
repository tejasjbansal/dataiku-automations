import dataikuapi
import os
from dotenv import load_dotenv

load_dotenv()

DSS_URL = os.environ["DSS_URL"]
API_KEY = os.environ["DSS_API_KEY"]
PROJECT_KEY = "ANALYTICAL_READY_DATASETS"

client = dataikuapi.DSSClient(DSS_URL, API_KEY)
project = client.get_project(PROJECT_KEY)

# Fix: restore the join condition
print("Fixing join_with_doctors: adding JOIN ON DOCTOR_ID...")
recipe = project.get_recipe("join_with_doctors")
settings = recipe.get_settings()
payload = settings.get_json_payload()
payload["joins"][0]["on"] = [{
    "column1": {"name": "DOCTOR_ID", "table": 0},
    "column2": {"name": "DOCTOR_ID", "table": 1},
    "type": "EQ"
}]
settings.set_json_payload(payload)
settings.save()
print("Fixed!")
