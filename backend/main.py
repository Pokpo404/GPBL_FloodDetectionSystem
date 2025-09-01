# backend/main.py
from fastapi import FastAPI
from backend.database import engine, Base
from backend.api import sensors, chat
import backend.models  # ensure models are imported so SQLAlchemy registers tables
from backend.models import SensorData, ChatMessage

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GPBL Flood Support API")

app.include_router(sensors.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "GPBL Flood Support Backend"}
