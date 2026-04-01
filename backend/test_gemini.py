import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('models/gemini-1.5-pro')
    response = model.generate_content("Say hello")
    print(f"Gemini 1.5 pro test success: {response.text}")
except Exception as e:
    print(f"Gemini 1.5 pro test failed: {e}")
