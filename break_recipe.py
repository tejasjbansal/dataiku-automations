import dataikuapi
import os
from dotenv import load_dotenv

load_dotenv()

DSS_URL = os.environ["DSS_URL"]
API_KEY = os.environ["DSS_API_KEY"]
PROJECT_KEY = "ANALYTICAL_READY_DATASETS"

client = dataikuapi.DSSClient(DSS_URL, API_KEY)
project = client.get_project(PROJECT_KEY)

# Intentionally break the join recipe by clearing the ON condition
print("Breaking join_with_doctors recipe (removing join condition)...")
recipe = project.get_recipe("join_with_doctors")
settings = recipe.get_settings()
payload = settings.get_json_payload()
payload["joins"][0]["on"] = []  # Empty = broken!
settings.set_json_payload(payload)
settings.save()
print("Done - recipe is now broken (empty join condition).")
