# backend/api/sensors.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db
from backend.services.google_sheets_service import GoogleSheetsService
import os

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.post("/", response_model=schemas.SensorDataOut, status_code=status.HTTP_201_CREATED)
def create_sensor(reading: schemas.SensorDataCreate, db: Session = Depends(get_db)):
    # duplicate check by timestamp + device_id
    exists = db.query(models.SensorData).filter_by(timestamp=reading.timestamp, device_id=reading.device_id).first()
    status_val = "normal"
    warning = float(os.getenv("WARNING_THRESHOLD_CM", "50"))
    critical = float(os.getenv("CRITICAL_THRESHOLD_CM", "20"))
    wl = reading.water_level
    if wl > warning:
        status_val = "normal"
    elif wl > critical:
        status_val = "warning"
    else:
        status_val = "critical"

    if exists:
        exists.water_level = reading.water_level
        exists.status = status_val
        exists.location = reading.location or exists.location
        exists.notes = reading.notes or exists.notes
        db.add(exists)
        db.commit()
        db.refresh(exists)
        return exists

    obj = models.SensorData(
        timestamp=reading.timestamp,
        device_id=reading.device_id,
        water_level=reading.water_level,
        location=reading.location or "Default Location",
        status=status_val,
        notes=reading.notes
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=List[schemas.SensorDataOut])
def list_sensors(limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.SensorData).order_by(models.SensorData.id.desc()).limit(limit).all()
    return items

@router.get("/data", response_model=List[schemas.SensorDataOut])
def get_sensor_data(limit: int = 100, db: Session = Depends(get_db)):
    """Alternative endpoint for frontend compatibility"""
    items = db.query(models.SensorData).order_by(models.SensorData.id.desc()).limit(limit).all()
    return items

@router.get("/latest", response_model=schemas.SensorDataOut)
def get_latest(db: Session = Depends(get_db)):
    item = db.query(models.SensorData).order_by(models.SensorData.id.desc()).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sensor data")
    return item

@router.get("/stats", response_model=schemas.StatisticsOut)
def get_stats(limit: int = 1000, db: Session = Depends(get_db)):
    items = db.query(models.SensorData).order_by(models.SensorData.id.desc()).limit(limit).all()
    if not items:
        return {
            "total_readings": 0,
            "average_water_level": 0,
            "max_water_level": 0,
            "min_water_level": 0,
            "devices": []
        }
    levels = [i.water_level for i in items]
    devices = list({i.device_id for i in items})
    return {
        "total_readings": len(items),
        "average_water_level": sum(levels) / len(levels),
        "max_water_level": max(levels),
        "min_water_level": min(levels),
        "devices": devices
    }

@router.post("/sync", status_code=status.HTTP_201_CREATED)
def sync_from_sheets(limit: int = 500, db: Session = Depends(get_db)):
    creds = os.getenv("GOOGLE_CREDENTIALS", "config/credentials.json")
    spreadsheet_id = os.getenv("SPREADSHEET_ID", None)
    sheet_name = os.getenv("SHEET_NAME", "Sheet1")
    allowed_device = os.getenv("ALLOWED_DEVICE", "waterlevel")
    gss = GoogleSheetsService(credentials_file=creds, spreadsheet_id=spreadsheet_id, sheet_name=sheet_name, allowed_device=allowed_device)
    sheet_items = gss.get_sensor_data(limit=limit)

    inserted = 0
    updated = 0
    for row in sheet_items:
        ts = row.get("timestamp")      # datetime obj
        device = row.get("device_id")
        wl = row.get("water_level")
        status_val = row.get("status")
        if ts is None or device is None or wl is None:
            continue
        # check existing by exact timestamp + device
        exists = db.query(models.SensorData).filter_by(timestamp=ts, device_id=device).first()
        if exists:
            if (exists.water_level != wl) or (exists.status != status_val):
                exists.water_level = wl
                exists.status = status_val
                db.add(exists)
                updated += 1
            continue
        obj = models.SensorData(timestamp=ts, device_id=device, water_level=wl, status=status_val)
        db.add(obj)
        inserted += 1
    db.commit()
    return {"inserted": inserted, "updated": updated, "total_from_sheet": len(sheet_items)}
