#!/usr/bin/env python3
"""
Add sample sensor data to database for testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, engine
from backend.models import Base, SensorData

def create_sample_data():
    """Create sample sensor data in database"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(SensorData).delete()
        db.commit()
        print("🗑️  Cleared existing sensor data")
        
        # Sample data generation
        devices = ['SENSOR_001', 'SENSOR_002', 'SENSOR_003']
        locations = ['Zone A - River Bridge', 'Zone B - Downtown', 'Zone C - Industrial Area']
        
        base_time = datetime.now()
        
        for i in range(50):
            device_idx = i % len(devices)
            
            # Generate realistic water levels
            base_level = random.uniform(0.5, 2.0)  # Normal range
            
            # Add some flooding scenarios in recent data
            if i < 10:  # Recent 10 readings might show flooding
                if random.random() < 0.3:  # 30% chance of high water
                    base_level = random.uniform(2.5, 4.0)
            
            # Determine status based on water level
            if base_level >= 3.0:
                status = 'critical'
            elif base_level >= 2.5:
                status = 'warning'
            else:
                status = 'normal'
            
            sensor_data = SensorData(
                device_id=devices[device_idx],
                water_level=round(base_level, 2),
                location=locations[device_idx],
                status=status,
                timestamp=base_time - timedelta(hours=i * 0.5)  # Data every 30 minutes
            )
            
            db.add(sensor_data)
        
        # Commit all data
        db.commit()
        print("✅ Added 50 sample sensor readings to database")
        
        # Show summary
        latest = db.query(SensorData).order_by(SensorData.timestamp.desc()).limit(5).all()
        print("\n📊 Latest 5 readings:")
        for i, reading in enumerate(latest, 1):
            print(f"  {i}. {reading.device_id}: {reading.water_level}m at {reading.location} - {reading.status}")
        
        # Count by status
        normal_count = db.query(SensorData).filter(SensorData.status == 'normal').count()
        warning_count = db.query(SensorData).filter(SensorData.status == 'warning').count()
        critical_count = db.query(SensorData).filter(SensorData.status == 'critical').count()
        
        print(f"\n📈 Data summary:")
        print(f"  Normal: {normal_count} readings")
        print(f"  Warning: {warning_count} readings")
        print(f"  Critical: {critical_count} readings")
        print(f"  Total: {normal_count + warning_count + critical_count} readings")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    print("🌊 FLOOD DETECTION SYSTEM - Sample Data Generator")
    print("=" * 55)
    create_sample_data()
    print("\n🎉 Sample data generation completed!")
    print("💡 You can now test the chatbot with real sensor data")
