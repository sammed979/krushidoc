import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from model import predict as model_predict

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an expert agricultural diagnostician for Indian farmers.
Respond ONLY in this exact JSON format, no extra text outside JSON:
{
  "crop": "crop common name",
  "disease_en": "disease common name in English",
  "disease_scientific": "scientific name",
  "disease_type": "Fungal | Bacterial | Viral | Nutrient Deficiency | Pest | Healthy",
  "confidence": 85,
  "severity": "Mild | Moderate | Critical",
  "revisit_days": "7-10 days",
  "yield_risk": "30-50%",
  "symptoms": [
    {"en": "short symptom point 1", "hi": "लक्षण 1"},
    {"en": "short symptom point 2", "hi": "लक्षण 2"},
    {"en": "short symptom point 3", "hi": "लक्षण 3"}
  ],
  "organic": [
    {"en": "short organic remedy 1", "hi": "जैविक उपाय 1"},
    {"en": "short organic remedy 2", "hi": "जैविक उपाय 2"}
  ],
  "chemical": [
    {"en": "chemical name + dosage 1", "hi": "दवा + मात्रा 1"},
    {"en": "chemical name + dosage 2", "hi": "दवा + मात्रा 2"}
  ]
}
Rules:
* Be practical and India-specific.
* Keep each point short and clear.
* Do not hallucinate. If unsure, say Unknown.
* Do not output anything outside JSON."""


def _parse_json(content: str) -> dict:
    content = content.strip()
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    return json.loads(content)


def _get_mime_type(image_bytes: bytes) -> str:
    if image_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if image_bytes[:3] == b'\xff\xd8\xff':
        return "image/jpeg"
    if image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
        return "image/webp"
    return "image/jpeg"


def analyze_crop_image(image_bytes: bytes):
    mime_type = _get_mime_type(image_bytes)
    print(f"Image size: {len(image_bytes)} bytes, MIME: {mime_type}")

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    # Use models with separate quotas as fallbacks
    models_to_try = [
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.0-flash-001",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
    ]
    last_error = None

    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=[SYSTEM_PROMPT, image_part]
            )
            raw = response.text
            print(f"Response from {model_name}: {raw[:300]}")
            result = _parse_json(raw)
            print(f"Success with {model_name}")

            # Run mock trained model alongside Gemini
            gemini_confidence = result.get("confidence", 80)
            model_result = model_predict(image_bytes, gemini_confidence)
            result["model_confidence"] = model_result["model_confidence"]
            result["combined_confidence"] = model_result["combined_confidence"]
            result["model_version"] = model_result["model_version"]
            result["dataset"] = model_result["dataset"]

            return result
        except Exception as e:
            last_error = str(e)
            print(f"Model {model_name} failed: {last_error}")
            # If quota exhausted wait 10 seconds before trying next model
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                import time
                print(f"Quota hit, waiting 10s before next model...")
                time.sleep(10)
            continue

    return {
        "error": "Failed to analyze image",
        "details": f"All models failed. Last error: {last_error}"
    }
