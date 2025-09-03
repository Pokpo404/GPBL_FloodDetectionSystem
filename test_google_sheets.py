#!/usr/bin/env python3
"""
Google Sheets Connection Test Script
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_sheets_connection():
    print("🔍 TESTING GOOGLE SHEETS CONNECTION...")
    print("=" * 50)
    
    # Check environment variables
    print("📋 Environment Variables:")
    spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID') or os.getenv('SPREADSHEET_ID')
    sheet_name = os.getenv('SHEET_NAME', 'Data')
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'config/credentials.json')
    
    print(f"   Spreadsheet ID: {spreadsheet_id}")
    print(f"   Sheet Name: {sheet_name}")
    print(f"   Credentials File: {credentials_file}")
    
    # Check credentials file
    print("\n🔐 Credentials File Check:")
    if os.path.exists(credentials_file):
        file_size = os.path.getsize(credentials_file)
        if file_size > 0:
            print(f"   ✅ File exists and has content ({file_size} bytes)")
        else:
            print(f"   ❌ File exists but is EMPTY!")
            return False
    else:
        print(f"   ❌ File does not exist: {credentials_file}")
        return False
    
    # Test Google Sheets Service
    print("\n🔗 Testing Google Sheets Service:")
    try:
        from backend.services.google_sheets_service import GoogleSheetsService
        
        # Initialize service
        gs_service = GoogleSheetsService(
            credentials_file=credentials_file,
            spreadsheet_id=spreadsheet_id,
            sheet_name=sheet_name
        )
        
        print("   ✅ GoogleSheetsService initialized successfully!")
        
        # Try to access the spreadsheet
        if gs_service.spreadsheet:
            print(f"   ✅ Connected to spreadsheet: {gs_service.spreadsheet.title}")
            
            # List worksheets
            worksheets = gs_service.spreadsheet.worksheets()
            print(f"   📄 Available worksheets: {[ws.title for ws in worksheets]}")
            
            # Try to read data
            try:
                data = gs_service.get_sensor_data(limit=5)
                if data:
                    print(f"   ✅ Successfully read {len(data)} sensor records")
                    print("   📊 Sample data:")
                    for i, record in enumerate(data[:3]):
                        print(f"      {i+1}. {record}")
                else:
                    print("   ⚠️  No sensor data found in sheet")
            except Exception as e:
                print(f"   ⚠️  Could not read sensor data: {e}")
                
        else:
            print("   ❌ Could not access spreadsheet")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n🎉 GOOGLE SHEETS CONNECTION TEST COMPLETED!")
    return True

def add_sample_data_to_sheets():
    """Add sample sensor data to Google Sheets"""
    print("\n📝 ADDING SAMPLE DATA TO GOOGLE SHEETS...")
    
    try:
        from backend.services.google_sheets_service import GoogleSheetsService
        from datetime import datetime, timedelta
        import random
        
        gs_service = GoogleSheetsService()
        
        # Sample data
        sample_data = []
        base_time = datetime.now()
        
        for i in range(5):
            data = {
                'device_id': f'SENSOR_{(i % 3) + 1:03d}',
                'water_level': round(random.uniform(0.5, 3.0), 2),
                'location': f'Zone {chr(65 + (i % 3))}',
                'status': 'normal',
                'timestamp': (base_time - timedelta(hours=i)).isoformat()
            }
            sample_data.append(data)
        
        # Add to sheets
        for data in sample_data:
            success = gs_service.add_sensor_reading(
                device_id=data['device_id'],
                water_level=data['water_level'], 
                location=data['location'],
                status=data['status'],
                timestamp=data['timestamp']
            )
            if success:
                print(f"   ✅ Added: {data['device_id']} - {data['water_level']}m")
            else:
                print(f"   ❌ Failed to add: {data['device_id']}")
                
    except Exception as e:
        print(f"   ❌ Error adding sample data: {e}")

if __name__ == "__main__":
    # Test connection
    success = test_google_sheets_connection()
    
    if success:
        # Optionally add sample data
        user_input = input("\n❓ Do you want to add sample sensor data to the sheet? (y/n): ")
        if user_input.lower() == 'y':
            add_sample_data_to_sheets()
    else:
        print("\n💡 NEXT STEPS:")
        print("1. Set up Google Cloud Console service account")
        print("2. Download credentials JSON file")  
        print("3. Place it in config/credentials.json")
        print("4. Share your Google Sheet with the service account email")
        print("5. Run this test again")
