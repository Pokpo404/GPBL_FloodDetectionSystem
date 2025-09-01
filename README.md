# 🌊 GPBL Flood Detection System - Backend


---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/GPBL_FloodDetectionSystem.git
   cd GPBL_FloodDetectionSystem
Create and activate a virtual environment:

```
python -m venv flood
source flood/Scripts/activate   # On Windows
source flood/bin/activate       # On Linux/Mac
``` 
Install dependencies:
```
pip install -r requirements.txt
```

Setup the database:
```
python backend/setup_database.py
```
▶️ Running the Backend

Run with Uvicorn:
```
uvicorn backend.main:app --reload
```

📡 API Testing

Once running, open your browser or use Postman:

Health check
```
GET http://127.0.0.1:8000/
```

Response:

{ "status": "ok", "service": "GPBL Flood Support Backend" }


Submit sensor data
```
POST http://127.0.0.1:8000/sensor-data/
```

Example body:

{
  "sensor_id": "sensor_01",
  "water_level": 85.5
}


Fetch all data

GET http://127.0.0.1:8000/sensor-data/