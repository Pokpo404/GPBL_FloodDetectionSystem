#!/usr/bin/env python3
"""
Database Setup Script for Flood Detection System
This script initializes the database and creates sample data
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import Base, engine, SessionLocal
from database import create_sensor_data, create_chat_message
from schemas import SensorDataCreate, ChatMessageCreate

def create_tables():
    """Create database tables"""
    print("🗄️ Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def create_sample_sensor_data():
    """Create sample sensor data for testing"""
    print("📊 Creating sample sensor data...")
    
    db = SessionLocal()
    try:
        # Create sample data for the last 30 days
        locations = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Can Tho", "Hai Phong"]
        
        for i in range(30):
            # Generate date (last 30 days)
            date = datetime.now() - timedelta(days=30-i)
            
            # Generate realistic water level data
            # Normal: 20-40cm, Warning: 50-80cm, Critical: 100-150cm
            if i < 20:
                water_level = random.uniform(20, 40)  # Normal
            elif i < 25:
                water_level = random.uniform(50, 80)  # Warning
            else:
                water_level = random.uniform(100, 150)  # Critical
            
            location = random.choice(locations)
            
            sensor_data = SensorDataCreate(
                water_level=round(water_level, 2),
                device_id=f"device_{i%5+1}",
                location=location,
                notes=f"Sample data for testing - Day {i+1}"
            )
            
            create_sensor_data(db, sensor_data)
        
        print(f"✅ Created 30 sample sensor readings")
        
    except Exception as e:
        print(f"❌ Error creating sample sensor data: {str(e)}")
    finally:
        db.close()

def create_sample_chat_data():
    """Create sample chat data for testing"""
    print("💬 Creating sample chat data...")
    
    db = SessionLocal()
    try:
        # Sample chat messages
        sample_messages = [
            "Mực nước hiện tại là bao nhiêu?",
            "Trạng thái hệ thống như thế nào?",
            "Cho tôi thống kê dữ liệu 7 ngày qua",
            "Có cảnh báo lũ lụt không?",
            "Hệ thống hoạt động bình thường chứ?",
            "Mực nước có tăng không?",
            "Cần làm gì khi có cảnh báo?",
            "Thời tiết hôm nay thế nào?",
            "Có dữ liệu mới nhất không?",
            "Hệ thống có ổn định không?"
        ]
        
        session_id = "sample_session_001"
        user_id = "test_user_001"
        
        for i, message in enumerate(sample_messages):
            chat_data = ChatMessageCreate(
                user_message=message,
                session_id=session_id,
                user_id=user_id
            )
            
            # Create chat message (this will also generate bot response)
            from api.chat import generate_llm_response
            bot_response = generate_llm_response(message, db)
            create_chat_message(db, chat_data, bot_response)
        
        print(f"✅ Created {len(sample_messages)} sample chat messages")
        
    except Exception as e:
        print(f"❌ Error creating sample chat data: {str(e)}")
    finally:
        db.close()

def main():
    """Main setup function"""
    print("🚀 Starting Flood Detection System Database Setup...")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
    # Create sample data
    create_sample_sensor_data()
    create_sample_chat_data()
    
    print("=" * 50)
    print("✅ Database setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy config/env_example.txt to config/.env")
    print("2. Configure your Google Sheets credentials")
    print("3. Run: python backend/main.py")
    print("4. Visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
