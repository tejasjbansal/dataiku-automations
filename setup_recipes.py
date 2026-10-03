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

# Clean up
for name in ["join_patients_prescriptions", "join_with_doctors", "group_rx_by_drug"]:
    try:
        project.get_recipe(name).delete()
    except:
        pass
for name in ["PATIENTS_PRESCRIPTIONS_joined", "PATIENT_DOCTOR_RX", "RX_BY_DRUG_SUMMARY"]:
    try:
        project.get_dataset(name).delete()
    except:
        pass

# --- Recipe 1: Join PATIENTS + PRESCRIPTIONS ---
print("1. Creating join recipe: PATIENTS + PRESCRIPTIONS...")
builder = project.new_recipe("join", "join_patients_prescriptions")
builder.with_input("PATIENTS")
builder.with_input("PRESCRIPTIONS")
builder.with_new_output("PATIENTS_PRESCRIPTIONS_joined", "filesystem_managed")
join_recipe = builder.build()

settings = join_recipe.get_settings()
# For join recipes, params must be added to the recipe_settings dict
settings.recipe_settings["params"] = {
    "joins": [{
        "table1": 0,
        "table2": 1,
        "conditionsMode": "AND",
        "type": "LEFT",
        "outerJoinOnTheLeft": True,
        "on": [{
            "column1": {"name": "PATIENT_ID", "table": 0},
            "column2": {"name": "PATIENT_ID", "table": 1},
            "type": "EQ"
        }]
    }],
    "virtualInputs": [
        {"index": 0, "preFilter": {"$and": []}},
        {"index": 1, "preFilter": {"$and": []}}
    ],
    "computedColumns": [],
    "postFilter": {"$and": []}
}
settings.save()
print("   Done -> PATIENTS_PRESCRIPTIONS_joined")

# --- Recipe 2: Join result + DOCTORS ---
print("\n2. Creating join recipe: joined + DOCTORS...")
builder2 = project.new_recipe("join", "join_with_doctors")
builder2.with_input("PATIENTS_PRESCRIPTIONS_joined")
builder2.with_input("DOCTORS")
builder2.with_new_output("PATIENT_DOCTOR_RX", "filesystem_managed")
join2_recipe = builder2.build()

settings2 = join2_recipe.get_settings()
settings2.recipe_settings["params"] = {
    "joins": [{
        "table1": 0,
        "table2": 1,
        "conditionsMode": "AND",
        "type": "LEFT",
        "outerJoinOnTheLeft": True,
        "on": [{
            "column1": {"name": "DOCTOR_ID", "table": 0},
            "column2": {"name": "DOCTOR_ID", "table": 1},
            "type": "EQ"
        }]
    }],
    "virtualInputs": [
        {"index": 0, "preFilter": {"$and": []}},
        {"index": 1, "preFilter": {"$and": []}}
    ],
    "computedColumns": [],
    "postFilter": {"$and": []}
}
settings2.save()
print("   Done -> PATIENT_DOCTOR_RX")

# --- Recipe 3: Group by drug ---
print("\n3. Creating group recipe: prescriptions by drug...")
builder3 = project.new_recipe("grouping", "group_rx_by_drug")
builder3.with_input("PATIENT_DOCTOR_RX")
builder3.with_new_output("RX_BY_DRUG_SUMMARY", "filesystem_managed")
group_recipe = builder3.build()

settings3 = group_recipe.get_settings()
settings3.recipe_settings["params"] = {
    "keys": [
        {"column": "DRUG_NAME", "type": "value"},
        {"column": "SPECIALTY", "type": "value"}
    ],
    "aggregations": [
        {"column": "PATIENT_ID", "function": "countDistinct"},
        {"column": "RX_ID", "function": "count"}
    ]
}
settings3.save()
print("   Done -> RX_BY_DRUG_SUMMARY")

print("\nAll 3 recipes created successfully!")
