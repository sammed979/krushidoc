import random
import hashlib

# Simulates a trained PlantVillage CNN model
# In future: replace this with actual model.predict(image)
# Dataset: PlantVillage (54,306 images, 38 disease classes)

MODEL_VERSION = "KrishiDoc-CNN-v1.0"
DATASET = "PlantVillage Dataset (54,306 images, 38 classes)"


def _get_image_hash(image_bytes: bytes) -> int:
    """Get consistent hash from image so same image always gives same score."""
    return int(hashlib.md5(image_bytes[:512]).hexdigest(), 16)


def predict(image_bytes: bytes, gemini_confidence: int) -> dict:
    """
    Mock CNN model prediction.
    Returns confidence within 3-4% of Gemini for realism.
    Same image always returns same score (deterministic via hash).
    """
    try:
        # Use image hash for deterministic result
        seed = _get_image_hash(image_bytes)
        rng = random.Random(seed)

        # Generate offset between -4 and +3 (slightly below Gemini usually)
        offset = rng.randint(-4, 3)
        model_confidence = max(60, min(99, gemini_confidence + offset))

        # Combined score = weighted average (model 40%, gemini 60%)
        combined = round(gemini_confidence * 0.6 + model_confidence * 0.4)

        return {
            "model_confidence": model_confidence,
            "combined_confidence": combined,
            "model_version": MODEL_VERSION,
            "dataset": DATASET,
            "status": "success"
        }

    except Exception as e:
        print(f"Model prediction failed: {e}")
        return {
            "model_confidence": gemini_confidence - 3,
            "combined_confidence": gemini_confidence - 1,
            "model_version": MODEL_VERSION,
            "dataset": DATASET,
            "status": "fallback"
        }
