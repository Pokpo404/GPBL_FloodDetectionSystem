# Flood Detection System

AI-powered real-time flood monitoring system with IoT sensors, web dashboard, and intelligent chatbot.

## Features

- **Real-time Monitoring**: Multi-zone water level tracking
- **AI Chatbot**: Google Gemini-powered flood assistant  
- **Web Dashboard**: Streamlit-based visualization
- **Alert System**: Automatic flood warnings (normal/warning/critical)
- **Data Integration**: Database + Google Sheets sync
- **Report Generation**: AI-powered flood analysis

## Quick Start

### 1. Setup Environment
```bash
git clone https://github.com/Pokpo404/GPBL_FloodDetectionSystem.git
cd GPBL_FloodDetectionSystem
python -m venv flood
flood\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Add Sample Data
```bash
python add_sample_data.py
```

### 3. Start Backend API
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 4. Start Frontend
```bash
streamlit run frontend/streamlit_simple.py
```

## Access Points

- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs  
- **Backend**: http://localhost:8000

## System Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   IoT Sensors   │───▶│   Backend    │───▶│   Frontend      │
│   (Simulated)   │    │   FastAPI    │    │   Streamlit     │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                       ┌──────▼──────┐
                       │  AI Chatbot │
                       │  (Gemini)   │
                       └─────────────┘
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/sensors/data` | Get sensor readings |
| GET | `/sensors/latest` | Latest sensor data |
| POST | `/chat/` | Chatbot interaction |
| GET | `/sensors/stats` | System statistics |

## Configuration

Create `.env` file:
```env
GEMINI_API_KEY=your_google_gemini_api_key
GOOGLE_SPREADSHEET_ID=your_sheet_id
WARNING_THRESHOLD_CM=250
CRITICAL_THRESHOLD_CM=300
```

## Testing

```bash
# System test
python test_system.py

# Chatbot test  
python test_chatbot.py

# Generate reports
python summarizer.py --mode daily --save
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Streamlit, Pandas, Plotly
- **AI**: Google Gemini API
- **Data**: Google Sheets API, Mock services
- **Deployment**: Uvicorn, Python 3.9+