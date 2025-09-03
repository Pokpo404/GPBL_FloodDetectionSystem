#!/usr/bin/env python3
"""
Simple chatbot test script
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_client import generate, generate_with_context

def test_greetings():
    """Test chatbot greeting responses"""
    
    greetings = [
        "Hi",
        "Hello",
        "Hey there!",
        "Good morning",
        "Xin chào"
    ]
    
    print("🤖 TESTING CHATBOT GREETINGS")
    print("=" * 40)
    
    for greeting in greetings:
        print(f"\n👤 User: {greeting}")
        print("🤖 Bot:", end=" ")
        
        try:
            # Test simple greeting
            response = generate(greeting)
            print(response[:100] + "..." if len(response) > 100 else response)
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 40)
    print("🧪 TESTING WITH SENSOR CONTEXT")
    
    # Mock sensor context
    sensor_context = """
Database sensor data:
- Latest water level: 2.8m at Zone A - River Bridge
- Status: warning
- Recent readings: 2.8m, 2.5m, 2.2m

Google Sheets sensor data:
- Latest reading: 3.1m at Zone A - River Bridge (warning)
- Alerts: 2 warnings/critical sensors
"""
    
    test_greeting = "Hi"
    print(f"\n👤 User: {test_greeting}")
    print("🤖 Bot with context:", end=" ")
    
    try:
        response = generate_with_context(test_greeting, sensor_context)
        print(response[:150] + "..." if len(response) > 150 else response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_greetings()
