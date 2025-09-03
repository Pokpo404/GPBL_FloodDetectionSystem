"""
Mock Google Sheets Service for Development
Use this when credentials.json is not available
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class MockGoogleSheetsService:
    """Mock service that simulates Google Sheets API responses"""
    
    def __init__(self, credentials_file=None, spreadsheet_id=None, sheet_name="Data"):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.mock_data = self._generate_mock_data()
        print(f"🔧 MockGoogleSheetsService initialized (Development Mode)")
    
    def _generate_mock_data(self) -> List[Dict]:
        """Generate realistic flood sensor data"""
        data = []
        base_time = datetime.now()
        
        devices = ['SENSOR_001', 'SENSOR_002', 'SENSOR_003']
        locations = ['Zone A - River Bridge', 'Zone B - Downtown', 'Zone C - Industrial Area']
        
        for i in range(20):
            # Simulate water levels with some variation
            base_level = random.uniform(0.5, 2.5)
            if i < 5:  # Recent data might show flooding
                base_level = random.uniform(2.0, 4.0)
            
            device_idx = i % len(devices)
            record = {
                'device_id': devices[device_idx],
                'water_level': round(base_level, 2),
                'location': locations[device_idx],
                'status': 'warning' if base_level > 2.5 else 'normal',
                'timestamp': (base_time - timedelta(hours=i * 0.5)).isoformat(),
                'battery': random.randint(60, 100),
                'signal_strength': random.randint(70, 100)
            }
            data.append(record)
        
        return sorted(data, key=lambda x: x['timestamp'], reverse=True)
    
    def get_sensor_data(self, limit: int = 10) -> List[Dict]:
        """Get latest sensor data"""
        return self.mock_data[:limit]
    
    def add_sensor_reading(self, device_id: str, water_level: float, 
                          location: str, status: str = "normal", 
                          timestamp: str = None) -> bool:
        """Add new sensor reading"""
        if not timestamp:
            timestamp = datetime.now().isoformat()
        
        new_reading = {
            'device_id': device_id,
            'water_level': water_level,
            'location': location,
            'status': status,
            'timestamp': timestamp,
            'battery': random.randint(60, 100),
            'signal_strength': random.randint(70, 100)
        }
        
        # Add to beginning of list (most recent first)
        self.mock_data.insert(0, new_reading)
        print(f"📝 Mock: Added sensor reading for {device_id}")
        return True
    
    def get_latest_alerts(self) -> List[Dict]:
        """Get sensors with warning/critical status"""
        alerts = []
        for reading in self.mock_data:
            if reading['status'] in ['warning', 'critical']:
                alerts.append(reading)
        return alerts[:5]  # Return max 5 alerts
    
    def get_historical_data(self, hours: int = 24) -> List[Dict]:
        """Get historical data for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        historical = []
        for reading in self.mock_data:
            reading_time = datetime.fromisoformat(reading['timestamp'].replace('Z', '+00:00'))
            if reading_time >= cutoff_time:
                historical.append(reading)
        
        return historical
    
    @property 
    def spreadsheet(self):
        """Mock spreadsheet object"""
        class MockSpreadsheet:
            title = "Flood Detection System - Mock Data"
            
            def worksheets(self):
                class MockWorksheet:
                    title = "Data"
                return [MockWorksheet()]
        
        return MockSpreadsheet()


def get_google_sheets_service():
    """Factory function to get appropriate Google Sheets service"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'config/credentials.json')
    
    # Check if credentials file exists and has content
    if os.path.exists(credentials_file) and os.path.getsize(credentials_file) > 0:
        try:
            from backend.services.google_sheets_service import GoogleSheetsService
            print("🔗 Using real Google Sheets service")
            return GoogleSheetsService()
        except Exception as e:
            print(f"⚠️  Google Sheets service failed, using mock: {e}")
            return MockGoogleSheetsService()
    else:
        print("🔧 Credentials not found, using mock Google Sheets service")
        return MockGoogleSheetsService()


if __name__ == "__main__":
    # Test the mock service
    mock_service = MockGoogleSheetsService()
    
    print("\n📊 Sample Mock Data:")
    data = mock_service.get_sensor_data(5)
    for i, reading in enumerate(data, 1):
        print(f"{i}. {reading['device_id']}: {reading['water_level']}m at {reading['location']} - {reading['status']}")
    
    print(f"\n🚨 Alerts: {len(mock_service.get_latest_alerts())} warnings/critical")
    print(f"📈 Historical data (24h): {len(mock_service.get_historical_data())} records")
