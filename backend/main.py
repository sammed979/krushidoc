import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from ai import analyze_crop_image
from whatsapp import handle_whatsapp_message
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="KrishiDoc API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "KrishiDoc API is running"}

# Web Diagnose Endpoint
@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    try:
        image_content = await file.read()
        diagnosis = analyze_crop_image(image_content)
        
        if "error" in diagnosis:
            raise HTTPException(status_code=500, detail=diagnosis["error"])
            
        return diagnosis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# WhatsApp Webhook Endpoint
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    response_twiml = handle_whatsapp_message(form_data)
    return Response(content=response_twiml, media_type="application/xml")

# Debug endpoint: test AI directly with an image URL
@app.get("/debug/test-ai")
async def debug_test_ai(image_url: str):
    import requests as req
    try:
        r = req.get(image_url, timeout=15)
        if r.status_code != 200:
            return {"error": f"Could not fetch image: HTTP {r.status_code}"}
        from ai import analyze_crop_image
        result = analyze_crop_image(r.content)
        return {"image_size": len(r.content), "result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
