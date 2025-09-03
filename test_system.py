#!/usr/bin/env python3
"""
Comprehensive System Test for Flood Detection System
"""

import requests
import json
from datetime import datetime

def test_backend_api():
    """Test all backend endpoints"""
    print("🔍 TESTING BACKEND API...")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint: OK")
        else:
            print(f"❌ Root endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint: {e}")
    
    # Test 2: Sensor data endpoint
    try:
        response = requests.get(f"{base_url}/sensors/data")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sensors data: {len(data)} records retrieved")
            if data:
                latest = data[0]
                print(f"   Latest: {latest['device_id']} - {latest['water_level']}m ({latest['status']})")
        else:
            print(f"❌ Sensors data: {response.status_code}")
    except Exception as e:
        print(f"❌ Sensors data: {e}")
    
    # Test 3: Latest sensor endpoint
    try:
        response = requests.get(f"{base_url}/sensors/latest")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Latest sensor: {data['device_id']} - {data['water_level']}m")
        else:
            print(f"❌ Latest sensor: {response.status_code}")
    except Exception as e:
        print(f"❌ Latest sensor: {e}")
    
    # Test 4: Statistics endpoint
    try:
        response = requests.get(f"{base_url}/sensors/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics: {stats['total_readings']} readings, avg {stats['average_water_level']:.2f}m")
        else:
            print(f"❌ Statistics: {response.status_code}")
    except Exception as e:
        print(f"❌ Statistics: {e}")

def test_chatbot():
    """Test chatbot with various queries"""
    print("\n🤖 TESTING CHATBOT...")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    test_queries = [
        "Hi, what's the current flood situation?",
        "Are there any flood warnings?", 
        "What's the water level at Zone A?",
        "Show me the latest sensor readings",
        "Is it safe to travel to downtown?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        try:
            payload = {"prompt": query, "max_tokens": 200}
            response = requests.post(f"{base_url}/chat/", json=payload)
            
            if response.status_code == 200:
                reply = response.json()["reply"]
                print(f"✅ Query {i}: {query[:30]}...")
                print(f"   Response: {reply[:100]}{'...' if len(reply) > 100 else ''}")
            else:
                print(f"❌ Query {i}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Query {i}: {e}")

def test_google_sheets_integration():
    """Test Google Sheets mock service"""
    print("\n📊 TESTING GOOGLE SHEETS INTEGRATION...")
    print("=" * 50)
    
    try:
        # Import and test mock service
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from backend.services.mock_google_sheets import get_google_sheets_service
        
        gs_service = get_google_sheets_service()
        
        # Test data retrieval
        data = gs_service.get_sensor_data(5)
        print(f"✅ Retrieved {len(data)} records from Google Sheets service")
        
        if data:
            print("   📋 Sample data:")
            for i, record in enumerate(data[:3], 1):
                print(f"      {i}. {record['device_id']}: {record['water_level']}m - {record['status']}")
        
        # Test alerts
        alerts = gs_service.get_latest_alerts()
        print(f"✅ Found {len(alerts)} active alerts")
        
        # Test historical data
        historical = gs_service.get_historical_data(24)
        print(f"✅ Historical data (24h): {len(historical)} records")
        
    except Exception as e:
        print(f"❌ Google Sheets integration: {e}")

def test_system_status():
    """Overall system health check"""
    print("\n🏥 SYSTEM HEALTH CHECK...")
    print("=" * 40)
    
    # Check if services are running
    services = {
        "Backend API": "http://localhost:8000/",
        "Frontend": "http://localhost:8501/"
    }
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service}: Running")
            else:
                print(f"⚠️  {service}: Status {response.status_code}")
        except Exception:
            print(f"❌ {service}: Not accessible")

if __name__ == "__main__":
    print("🌊 FLOOD DETECTION SYSTEM - COMPREHENSIVE TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_system_status()
    test_backend_api()
    test_google_sheets_integration()
    test_chatbot()
    
    print("\n🎉 TESTING COMPLETED!")
    print("💡 If all tests pass, your flood detection system is ready!")
    print("🌐 Frontend: http://localhost:8501")
    print("🔧 API Docs: http://localhost:8000/docs")
