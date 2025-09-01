# backend/models.py
from sqlalchemy import Column, Integer, Float, String, DateTime, Text, func
from .database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    water_level = Column(Float, nullable=False)  # store distance_cm as float
    timestamp = Column(DateTime, nullable=False, index=True)
    device_id = Column(String(100), nullable=False, index=True, default="waterlevel")
    location = Column(String(100), default="Default Location")
    status = Column(String(20), default="normal")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    session_id = Column(String(100), nullable=True)
    user_id = Column(String(100), nullable=True)
