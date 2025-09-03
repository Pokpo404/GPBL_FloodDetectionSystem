# backend/api/chat.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import importlib
from backend.database import get_db
from backend import models

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 256

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Get latest sensor data from both database and Google Sheets
    sensor_context = ""
    
    try:
        # Try database first
        latest_sensors = db.query(models.SensorData).order_by(models.SensorData.timestamp.desc()).limit(5).all()
        
        if latest_sensors:
            latest = latest_sensors[0]
            sensor_context += f"""
Database sensor data:
- Latest water level: {latest.water_level}m at {latest.location}
- Status: {latest.status}
- Timestamp: {latest.timestamp}
- Recent readings: {', '.join([f"{s.water_level}m" for s in latest_sensors[:3]])}
"""
        
        # Also try Google Sheets data
        try:
            from backend.services.mock_google_sheets import get_google_sheets_service
            gs_service = get_google_sheets_service()
            sheets_data = gs_service.get_sensor_data(3)
            
            if sheets_data:
                sensor_context += f"""
Google Sheets sensor data:
- Latest reading: {sheets_data[0]['water_level']}m at {sheets_data[0]['location']} ({sheets_data[0]['status']})
- Recent levels: {', '.join([f"{d['water_level']}m" for d in sheets_data])}
- Alerts: {len(gs_service.get_latest_alerts())} warnings/critical sensors
"""
        except Exception as e:
            sensor_context += f"\nGoogle Sheets: {str(e)}"
            
        if not sensor_context.strip():
            sensor_context = "No current sensor data available from any source."
            
    except Exception as e:
        sensor_context = f"Error retrieving sensor data: {str(e)}"
    
    # Try to call llm_client.generate with sensor context
    try:
        lc = importlib.import_module("llm_client")
        if hasattr(lc, "generate_with_context"):
            out = lc.generate_with_context(request.prompt, sensor_context, max_tokens=request.max_tokens)
            return {"reply": out}
        elif hasattr(lc, "generate"):
            # Fallback to old method
            enhanced_prompt = f"Sensor data: {sensor_context}\n\nUser question: {request.prompt}"
            out = lc.generate(enhanced_prompt, max_tokens=request.max_tokens)
            return {"reply": out}
    except Exception as e:
        pass
    
    # fallback
    return {"reply": f"[LLM not configured] Echo: {request.prompt}"}
