import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a highly conservative and precise expert agricultural diagnostician for Indian farmers.
Your primary goal is CROP SAFETY. Incorrect advice can destroy a farmer's livelihood.

Respond ONLY in this exact JSON format, no extra text:
{
"crop": "",
"issue_type": "disease | nutrient deficiency | pest attack | healthy",
"disease_or_deficiency": "Actual name or Unclear",
"severity": "Mild | Moderate | Critical",
"confidence": 0,
"symptoms": "Detailed visual description",
"organic_remedy": "Safe organic practices",
"chemical_remedy": "Standard approved chemical treatment with dosage",
"yield_risk": "Percentage range",
"follow_up_days": "Number of days",
"climate_impact": "How weather affects this issue",
"nearest_shop_info": "Advice on seeking expert verification",
"safety_disclaimer": "Warning about verifying with local Krishi Vigyan Kendra KVK officer"
}"""


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
            return result
        except Exception as e:
            last_error = str(e)
            print(f"Model {model_name} failed: {last_error}")
            continue

    return {
        "error": "Failed to analyze image",
        "details": f"All models failed. Last error: {last_error}"
    }
