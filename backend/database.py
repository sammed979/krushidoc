import os
import base64
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


def save_diagnosis(diagnosis: dict, source: str = "web", image_bytes: bytes = None):
    try:
        col = get_collection()
        if col is None:
            return

        disease_name = (
            diagnosis.get("disease_en") or
            diagnosis.get("disease_or_deficiency") or
            "Unknown"
        )

        record = {
            "timestamp": datetime.utcnow(),
            "source": source,
            "crop": diagnosis.get("crop", "Unknown"),
            "disease_name": disease_name,
            "disease_scientific": diagnosis.get("disease_scientific", "Unknown"),
            "disease_type": diagnosis.get("disease_type", diagnosis.get("issue_type", "Unknown")),
            "severity": diagnosis.get("severity", "Unknown"),
            "confidence": diagnosis.get("confidence", 0),
            "yield_risk": diagnosis.get("yield_risk", "Unknown"),
            "revisit_days": diagnosis.get("revisit_days", diagnosis.get("follow_up_days", "Unknown")),
        }

        # Save image as base64 if provided
        if image_bytes:
            record["image_base64"] = base64.b64encode(image_bytes).decode("utf-8")
            record["image_size_kb"] = round(len(image_bytes) / 1024, 2)

        col.insert_one(record)
        print(f"Saved to MongoDB: {record['crop']} - {record['disease_name']} (image: {'yes' if image_bytes else 'no'})")

    except Exception as e:
        print(f"Failed to save to MongoDB: {e}")
