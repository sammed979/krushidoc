import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = None
collection = None

def get_collection():
    global client, collection
    if collection is None:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            db = client["krushidoc"]
            collection = db["diagnoses"]
            print("MongoDB connected successfully")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            collection = None
    return collection


def save_diagnosis(diagnosis: dict, source: str = "web"):
    try:
        col = get_collection()
        if col is None:
            return

        record = {
            "timestamp": datetime.utcnow(),
            "source": source,
            "crop": diagnosis.get("crop", "Unknown"),
            "disease_en": diagnosis.get("disease_en", diagnosis.get("disease_or_deficiency", "Unknown")),
            "disease_scientific": diagnosis.get("disease_scientific", "Unknown"),
            "disease_type": diagnosis.get("disease_type", diagnosis.get("issue_type", "Unknown")),
            "severity": diagnosis.get("severity", "Unknown"),
            "confidence": diagnosis.get("confidence", 0),
            "yield_risk": diagnosis.get("yield_risk", "Unknown"),
            "revisit_days": diagnosis.get("revisit_days", diagnosis.get("follow_up_days", "Unknown")),
        }

        col.insert_one(record)
        print(f"Diagnosis saved to MongoDB: {record['crop']} - {record['disease_en']}")

    except Exception as e:
        print(f"Failed to save diagnosis to MongoDB: {e}")
