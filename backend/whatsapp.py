import os
import requests
import traceback
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from ai import analyze_crop_image
from database import save_diagnosis
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def _send_whatsapp(to: str, body: str):
    """Send WhatsApp message via Twilio REST API (no session timeout issue)."""
    try:
        twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to,
            body=body
        )
        print(f"Message sent to {to}")
    except Exception as e:
        print(f"Failed to send message: {e}")


def _download_image(media_url: str) -> bytes | None:
    for attempt in range(3):
        try:
            print(f"Download attempt {attempt + 1} for: {media_url}")
            r = requests.get(
                media_url,
                auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                timeout=20,
                headers={"User-Agent": "KrishiDoc/1.0"}
            )
            print(f"Download status: {r.status_code}, size: {len(r.content)} bytes")
            if r.status_code == 200 and len(r.content) > 1000:
                return r.content
            print(f"Bad response: status={r.status_code}, body={r.text[:200]}")
        except Exception as e:
            print(f"Download attempt {attempt + 1} failed: {e}")
    return None


def _format_list(items, key_en='en', key_hi='hi') -> str:
    """Format bilingual array into WhatsApp bullet points."""
    if not isinstance(items, list):
        return str(items)
    lines = []
    for item in items:
        if isinstance(item, dict):
            lines.append(f"• {item.get(key_en, '')}\n  {item.get(key_hi, '')}")
        else:
            lines.append(f"• {item}")
    return "\n".join(lines)


def _format_diagnosis(diagnosis: dict) -> str:
    crop = diagnosis.get('crop', 'Unknown')
    disease = diagnosis.get('disease_en', diagnosis.get('disease_or_deficiency', 'Unknown'))
    disease_type = diagnosis.get('disease_type', diagnosis.get('issue_type', 'Unknown'))
    severity = diagnosis.get('severity', 'Unknown')
    confidence = diagnosis.get('confidence', 0)
    yield_risk = diagnosis.get('yield_risk', 'Unknown')
    revisit = diagnosis.get('revisit_days', diagnosis.get('follow_up_days', '7-10 days'))

    symptoms = _format_list(diagnosis.get('symptoms', []))
    organic = _format_list(diagnosis.get('organic', []))
    chemical = _format_list(diagnosis.get('chemical', []))

    return (
        f"🌿 *KrishiDoc Report*\n"
        f"🌾 *Crop / फसल:* {crop}\n"
        f"🩺 *Disease / रोग:* {disease} ({disease_type})\n"
        f"⚠️ *Severity / गंभीरता:* {severity}\n"
        f"📊 *Confidence / विश्वास:* {confidence}%\n"
        f"📉 *Yield Risk / उपज हानि:* {yield_risk}\n"
        f"📅 *Revisit / दोबारा जांच:* {revisit}\n\n"
        f"🔍 *Symptoms / लक्षण:*\n{symptoms}\n\n"
        f"🍃 *Organic / जैविक:*\n{organic}\n\n"
        f"🧪 *Chemical / रासायनिक:*\n{chemical}\n\n"
        f"⚠️ _KVK officer से सत्यापित करें / Verify with KVK officer._"
    )


def handle_whatsapp_message(request_form):
    print("\n--- NEW WHATSAPP MESSAGE ---")
    print(f"Form Data: {dict(request_form)}")

    # Always return empty TwiML immediately — reply via REST API instead
    empty_response = str(MessagingResponse())

    from_number = request_form.get('From', '')
    num_media = int(request_form.get('NumMedia', 0))
    print(f"From: {from_number}, Media items: {num_media}")

    if num_media == 0:
        _send_whatsapp(from_number, "Welcome to *KrishiDoc*! 🌿\nSend a crop leaf photo 📸 for instant AI diagnosis.")
        return empty_response

    media_url = request_form.get('MediaUrl0')
    content_type = request_form.get('MediaContentType0', '')
    print(f"Media URL: {media_url}, Content-Type: {content_type}")

    if not content_type.startswith('image/'):
        _send_whatsapp(from_number, "Please send a crop leaf *image* 📸 (JPG/PNG).")
        return empty_response

    try:
        # Send immediate acknowledgement so user knows it's processing
        _send_whatsapp(from_number, "🔍 Analyzing your crop image... Please wait.")

        image_bytes = _download_image(media_url)

        if not image_bytes:
            _send_whatsapp(from_number, "⚠️ Could not download your image. Please try sending it again.")
            return empty_response

        print(f"Analyzing image ({len(image_bytes)} bytes)...")
        diagnosis = analyze_crop_image(image_bytes)
        print(f"Diagnosis result keys: {list(diagnosis.keys())}")

        if "error" in diagnosis:
            print(f"AI Error: {diagnosis['error']} | Details: {diagnosis.get('details', '')}")
            _send_whatsapp(from_number,
                f"⚠️ Could not analyze this image.\n\n"
                f"Please try:\n• A clearer, well-lit photo\n• Closer shot of the affected leaf\n• JPG or PNG format"
            )
        else:
            save_diagnosis(diagnosis, source="whatsapp")
            reply = _format_diagnosis(diagnosis)
            print(f"Reply length: {len(reply)} chars")
            _send_whatsapp(from_number, reply)

    except Exception as e:
        print(f"CRITICAL ERROR:\n{traceback.format_exc()}")
        _send_whatsapp(from_number, f"⚠️ System error. Please try again.")

    return empty_response
