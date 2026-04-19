# 🌿 KrishiDoc — AI Crop Doctor

> Empowering Indian Farmers with Artificial Intelligence

[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://krushidoc.vercel.app/)
[![Backend](https://img.shields.io/badge/Backend-Render-blue)](https://krushidoc.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-krushidoc-black)](https://github.com/sammed979/krushidoc)

---

## 🌐 Live Links

| Service | URL |
|---------|-----|
| 🌐 Web App | https://krushidoc.vercel.app/ |
| ⚙️ Backend API | https://krushidoc.onrender.com/ |
| 📱 WhatsApp Bot | +1 415 523 8886 |

---

## 📌 What is KrishiDoc?

KrishiDoc is an AI-powered crop disease diagnosis system built for Indian farmers. Farmers can upload a crop leaf image via **Web** or **WhatsApp** and instantly receive a detailed diagnosis in both **Hindi and English** — including disease name, severity, organic remedy, chemical remedy, and yield risk.

---

## ✨ Features

- 🤖 **Dual AI Analysis** — Google Gemini AI + KrishiDoc CNN Model
- 🌾 **Crop Disease Diagnosis** — Identifies disease, severity, yield risk
- 🇮🇳 **Bilingual Results** — Hindi + English output
- 📱 **WhatsApp Bot** — Send crop image on WhatsApp, get instant diagnosis
- 🌐 **Web Analysis** — Upload image on website for detailed report
- 📊 **MongoDB Dataset** — Every diagnosis saved for government data sharing
- 🖼️ **Image Storage** — Farmer images stored with disease data
- 🔬 **Scientific Names** — Disease scientific name included
- 💊 **Remedies** — Both organic and chemical remedies with dosage
- ⚠️ **Safety Warnings** — KVK officer verification reminders

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI Model | Google Gemini API (gemini-2.5-flash) |
| Mock CNN | KrishiDoc-CNN-v1.0 (PlantVillage Dataset) |
| Database | MongoDB Atlas |
| Messaging | Twilio WhatsApp API |
| Deployment | Vercel (Frontend), Render (Backend) |

---

## 🚀 How to Use

### 🌐 Web Analysis
1. Open https://krushidoc.vercel.app/
2. Click **"Web Analysis"**
3. Upload a clear crop leaf image (JPG/PNG)
4. Click **"Analyze Crop Health"**
5. Get instant bilingual diagnosis report

### 📱 WhatsApp Bot
1. Open WhatsApp
2. Send message to **+1 415 523 8886**
3. Type `join none-younger` to join sandbox
4. Send a crop leaf photo 📸
5. Receive instant AI diagnosis in Hindi + English

---

## 📊 Sample Output

```
🌿 KrishiDoc Report

🌾 Crop / फसल: Cotton
🩺 Disease / रोग: Alternaria Leaf Spot (Fungal)
⚠️ Severity / गंभीरता: Moderate
📊 Confidence / विश्वास: 90%
📉 Yield Risk / उपज हानि: 15-35%
📅 Revisit / दोबारा जांच: 7-10 days

🔍 Symptoms / लक्षण:
• Dark brown circular spots on leaves
  पत्तियों पर गहरे भूरे गोल धब्बे

🍃 Organic / जैविक:
• Spray neem oil weekly
  नीम तेल साप्ताहिक छिड़कें

🧪 Chemical / रासायनिक:
• Mancozeb 75% WP @ 2.5g/L
  मैन्कोज़ेब 75% WP @ 2.5g/L
```

---

## 🗄️ Dataset

```
dataset/
├── healthy/          → Healthy crop images
└── diseases/
    ├── chilli/       → 10 images
    ├── cotton/       → 10 images
    ├── grapes/       → 10 images
    ├── sugercane/    → 10 images
    └── tomato/       → 10 images
```

- Source: PlantVillage Dataset (54,306 images, 38 classes)
- Future: Retrain with Indian farm images from MongoDB

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Node.js (optional for frontend)
- MongoDB Atlas account
- Google Gemini API key
- Twilio account

### Backend Setup
```bash
# Clone repo
git clone https://github.com/sammed979/krushidoc.git
cd krushidoc/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env

# Run server
python main.py
```

### Frontend Setup
```bash
# Open frontend folder
cd krushidoc/frontend

# Open index.html in browser
# OR serve with live server
```

### Environment Variables
```env
GEMINI_API_KEY=your_gemini_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
MONGO_URI=your_mongodb_connection_string
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/diagnose` | Web image diagnosis |
| POST | `/webhook/whatsapp` | WhatsApp webhook |
| GET | `/debug/test-ai?image_url=` | Test AI with URL |

---

## 🏗️ Project Structure

```
krushidoc/
├── backend/
│   ├── main.py          → FastAPI server
│   ├── ai.py            → Gemini AI integration
│   ├── whatsapp.py      → WhatsApp bot logic
│   ├── database.py      → MongoDB integration
│   ├── model.py         → KrishiDoc CNN mock model
│   ├── train.py         → Training pipeline (future)
│   └── requirements.txt
├── frontend/
│   ├── index.html       → Landing page
│   ├── analyze.html     → Analysis page
│   ├── script.js        → Frontend logic
│   └── style.css        → Styling
├── dataset/
│   ├── README.md        → Dataset instructions
│   ├── healthy/         → Healthy crop images
│   └── diseases/        → Disease crop images
└── README.md
```

---

## 🤖 Dual AI Architecture

```
Farmer sends image
        ↓
┌─────────────────────────┐
│   Google Gemini AI      │ → Detailed diagnosis
│   (gemini-2.5-flash)    │   Hindi + English
└─────────────────────────┘
        +
┌─────────────────────────┐
│   KrishiDoc CNN v1.0    │ → Confidence score
│   (PlantVillage)        │   Cross validation
└─────────────────────────┘
        ↓
   Combined Result
   Sent to Farmer
```

---

## 🌱 Future Plans

- [ ] Train KrishiDoc-CNN-v1.0 on collected Indian farm images
- [ ] Add more regional languages (Kannada, Marathi, Telugu)
- [ ] Government data dashboard
- [ ] Offline mode for rural areas
- [ ] Weather-based disease prediction
- [ ] Nearby Krishi Kendra locator

---

## 👨‍💻 Built By

**Sam Padanad** — KrishiDoc AI
> Built for the future of Indian agriculture 🌾

---

## ⚠️ Disclaimer

KrishiDoc AI analysis is for guidance only. Always verify diagnosis with a local **Krishi Vigyan Kendra (KVK)** officer before applying any treatment.
