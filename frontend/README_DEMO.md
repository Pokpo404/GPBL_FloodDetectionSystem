# 🌊 DEMO Frontend - GPBL Flood Detection System

## 📋 Step-by-Step Demo Guide

### 🚀 Method 1: Auto Run (Simplest)
```bash
# Just double-click this file:
run_demo.bat
```

### 🔧 Method 2: Manual Step-by-Step

#### Step 1: Activate Environment
```bash
cd D:\gBL_DiasterSupport\GPBL_FloodDetectionSystem
flood\Scripts\activate
```

#### Step 2: Run Backend
```bash
uvicorn backend.main:app --reload --port 8000
```

#### Step 3: Run Frontend (New Terminal)
```bash
streamlit run frontend\streamlit_simple.py --server.port 8502
```

## 🌐 Access Applications

- **Frontend (Streamlit)**: http://localhost:8502
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✨ Demo Features

### 📊 Dashboard
- Real-time water level display
- Danger/safe alerts
- Sensor data table

### 🤖 AI Chatbot
- Flood-related Q&A
- Gemini AI integration
- User-friendly chat interface

### 📈 Charts
- 24h water level chart
- Temperature & humidity over time
- Overview statistics

### ⚙️ Settings
- Backend connection test
- System information

## 🎯 Demo for Instructors

1. **Open frontend**: Show dashboard overview
2. **Explain dashboard**: Water level, alerts, sensor data
3. **Demo chatbot**: Ask "What's the current water level situation?"
4. **View charts**: Analyze data trends
5. **Check backend**: API working stably

## 🛠️ Technology Stack

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: Streamlit + Pandas
- **AI**: Google Gemini API
- **Database**: SQLite
- **Deployment**: Local development

## 📱 Demo Interface

```
🌊 IoT Flood Detection System
├── 📊 Dashboard (Main page)
├── 🤖 Chatbot (AI Support)  
├── 📈 Charts (Analysis)
└── ⚙️ Settings (Information)
```

## 🎨 Highlights

✅ **Modern UI**: Clean interface with Streamlit  
✅ **Responsive**: Auto-adjusts to screen size  
✅ **Real-time**: Live data updates  
✅ **AI Integration**: Smart chatbot  
✅ **Data Visualization**: Interactive charts  
✅ **English Interface**: Professional presentation  

## 🔍 Troubleshooting

### Backend not running:
```bash
# Check if port 8000 is occupied
netstat -ano | findstr :8000
```

### Frontend not running:
```bash
# Reinstall Streamlit
pip install --upgrade streamlit
```

### Database connection error:
```bash
# Recreate database
python scripts/setup_database.py
```

---
**Good luck with your demo! 🎉**
