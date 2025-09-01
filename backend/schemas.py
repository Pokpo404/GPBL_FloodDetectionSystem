# backend/schemas.py
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from dateutil import parser as _dateutil_parser

# ---------- Input when device/posts new reading ----------
class SensorDataCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # use attributes from ORM objects

    timestamp: datetime = Field(..., description="Timestamp ISO or common format")
    device_id: str = Field(..., description="Device id, e.g. 'waterlevel'")
    water_level: float = Field(..., ge=0, description="Distance in cm from sensor to water")
    location: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("timestamp", mode="before")
    @classmethod
    def _parse_timestamp(cls, v):
        if isinstance(v, datetime):
            return v
        s = str(v).strip()
        # try common formats quickly
        fmts = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y-%m-%d")
        for f in fmts:
            try:
                return datetime.strptime(s, f)
            except Exception:
                pass
        # fallback to dateutil
        try:
            return _dateutil_parser.parse(s)
        except Exception:
            raise ValueError("Unsupported timestamp format")

# ---------- Output returned to clients ----------
class SensorDataOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    device_id: str
    water_level: float
    location: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

# ---------- Stats response ----------
class StatisticsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_readings: int
    average_water_level: float
    max_water_level: float
    min_water_level: float
    devices: List[str]

# ---------- Chat schemas ----------
class ChatMessageCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_message: str
    bot_response: str
    timestamp: datetime
    session_id: Optional[str]
    user_id: Optional[str]

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 256

class ChatResponse(BaseModel):
    reply: str
