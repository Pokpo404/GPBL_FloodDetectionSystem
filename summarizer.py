import google.generativeai as genai
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.database import SessionLocal
    from backend.models import SensorData
    from backend.services.mock_google_sheets import get_google_sheets_service
except ImportError as e:
    print(f"Warning: Could not import backend modules: {e}")
    SessionLocal = None
    SensorData = None
    get_google_sheets_service = None

class Summarizer:
    
    # LLM initialization
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Initialize database connection if available
        if SessionLocal:
            self.db = SessionLocal()
            self.gs_service = get_google_sheets_service()
        else:
            self.db = None
            self.gs_service = None

    # Summarization helper function
    def summarize(self, text: str, style: str = "concise") -> str:
        """
        Summarize input text.
        :param text: Raw text to summarize
        :param style: 'concise', 'detailed', or 'bullet points'
        :return: Summary string
        """
        prompt = f"Summarize the following text in a {style} way:\n\n{text}"
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    #summarizer with json input
    def summarize_json(self, data: dict, style="concise"):
        """
        Summarize flood sensor data from JSON format.

        Expected JSON format:
        {
            "records": [
                {
                    "timestamp": "2025-08-30T14:00:00",
                    "sensor_1": 2.3,
                    "sensor_2": 2.1
                },
                {
                    "timestamp": "2025-08-30T15:00:00",
                    "sensor_1": 2.7,
                    "sensor_2": 2.5
                },
                ...
            ]
        }

        Parameters:
        - data (dict): JSON-like dictionary containing multiple flood sensor readings.
        - style (str): Summary style (e.g., "concise", "detailed", "alert-focused").

        Returns:
        - str: A summarized report of water level trends and risks.
        """
        prompt = f"""
        Summarize this flood report in a {style} way:

        {data}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def get_flood_data_summary(self, hours: int = 24) -> Dict:
        """Get flood sensor data summary from database and Google Sheets"""
        if not self.db or not self.gs_service:
            return {"error": "Database connection not available"}
        
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Database data
            db_readings = self.db.query(SensorData).filter(
                SensorData.timestamp >= cutoff_time
            ).order_by(SensorData.timestamp.desc()).all()
            
            # Google Sheets data
            gs_data = self.gs_service.get_historical_data(hours)
            
            summary = {
                'time_range': f"Last {hours} hours",
                'timestamp': datetime.now().isoformat(),
                'database_readings': len(db_readings),
                'sheets_readings': len(gs_data),
                'zones': {},
                'alerts': {'critical': 0, 'warning': 0, 'normal': 0},
                'max_level': 0,
                'min_level': float('inf') if db_readings else 0
            }
            
            # Analyze database readings
            for reading in db_readings:
                zone = reading.location
                if zone not in summary['zones']:
                    summary['zones'][zone] = {
                        'current_level': reading.water_level,
                        'max_level': reading.water_level,
                        'min_level': reading.water_level,
                        'status': reading.status,
                        'device_id': reading.device_id,
                        'readings_count': 0
                    }
                
                zone_data = summary['zones'][zone]
                zone_data['readings_count'] += 1
                zone_data['max_level'] = max(zone_data['max_level'], reading.water_level)
                zone_data['min_level'] = min(zone_data['min_level'], reading.water_level)
                
                summary['max_level'] = max(summary['max_level'], reading.water_level)
                if summary['min_level'] != float('inf'):
                    summary['min_level'] = min(summary['min_level'], reading.water_level)
                summary['alerts'][reading.status] += 1
            
            return summary
            
        except Exception as e:
            return {"error": f"Failed to get flood data: {e}"}
    
    def summarize_flood_situation(self, hours: int = 24, style: str = "detailed") -> str:
        """Generate AI summary of current flood situation"""
        data = self.get_flood_data_summary(hours)
        
        if "error" in data:
            return f"❌ {data['error']}"
        
        # Prepare context for AI
        context = f"""
🌊 FLOOD DETECTION SYSTEM DATA ({hours}h):

📊 DATA OVERVIEW:
- Database readings: {data['database_readings']}
- Google Sheets readings: {data['sheets_readings']}
- Monitoring period: {data['time_range']}

🏘️ ZONES STATUS:
"""
        
        for zone, zone_data in data['zones'].items():
            status_emoji = {"critical": "🔴", "warning": "🟡", "normal": "🟢"}.get(zone_data['status'], "⚪")
            context += f"""
{status_emoji} {zone}:
  • Current: {zone_data['current_level']}m ({zone_data['status']})
  • Range: {zone_data['min_level']:.2f}m - {zone_data['max_level']:.2f}m
  • Device: {zone_data['device_id']}
  • Readings: {zone_data['readings_count']}
"""
        
        context += f"""
🚨 ALERT SUMMARY:
• Critical: {data['alerts']['critical']} readings
• Warning: {data['alerts']['warning']} readings
• Normal: {data['alerts']['normal']} readings

📈 SYSTEM RANGE:
• Maximum level: {data['max_level']}m
• Minimum level: {data['min_level']}m
"""
        
        prompt = f"""
You are a flood monitoring AI assistant. Based on the sensor data, provide a {style} summary report including:

1. 🎯 CURRENT SITUATION: Overall flood risk assessment
2. 📍 ZONE ANALYSIS: Status of each monitoring area
3. 📊 TRENDS: Notable patterns or changes
4. ⚠️ RECOMMENDATIONS: Actions for authorities and residents
5. 🚨 PRIORITY ALERTS: Critical areas needing attention

Write in a professional yet accessible manner for both emergency teams and the public.
Use clear sections and relevant emojis for better readability.

Sensor Data Context:
{context}
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"❌ Error generating AI summary: {e}\n\n📋 Raw data:\n{json.dumps(data, indent=2)}"
    
    def generate_alert_report(self) -> str:
        """Generate focused alert report for critical situations"""
        if not self.db or not self.gs_service:
            return "❌ Database connection not available for alert generation"
        
        try:
            # Get recent critical/warning readings
            recent_alerts = self.db.query(SensorData).filter(
                SensorData.status.in_(['critical', 'warning']),
                SensorData.timestamp >= datetime.now() - timedelta(hours=6)
            ).order_by(SensorData.timestamp.desc()).limit(10).all()
            
            # Get Google Sheets alerts
            gs_alerts = self.gs_service.get_latest_alerts()
            
            if not recent_alerts and not gs_alerts:
                return "✅ NO ACTIVE FLOOD ALERTS\nAll monitoring zones report normal water levels."
            
            alert_text = "🚨 FLOOD ALERT REPORT\n" + "="*50 + f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if recent_alerts:
                alert_text += "📊 DATABASE ALERTS (Last 6 hours):\n"
                for alert in recent_alerts:
                    emoji = "🔴" if alert.status == 'critical' else "🟡"
                    time_str = alert.timestamp.strftime('%H:%M')
                    alert_text += f"{emoji} {alert.location}: {alert.water_level}m ({alert.status.upper()}) at {time_str}\n"
                alert_text += "\n"
            
            if gs_alerts:
                alert_text += f"📋 GOOGLE SHEETS ALERTS: {len(gs_alerts)} active warnings\n"
                for alert in gs_alerts[:5]:  # Show top 5
                    emoji = "🔴" if alert['status'] == 'critical' else "🟡"
                    alert_text += f"{emoji} {alert['location']}: {alert['water_level']}m ({alert['status'].upper()})\n"
            
            return alert_text
            
        except Exception as e:
            return f"❌ Error generating alert report: {e}"
    
    def generate_daily_report(self) -> str:
        """Generate comprehensive daily flood monitoring report"""
        print("🏗️ Generating daily flood monitoring report...")
        
        report = f"""
🌊 DAILY FLOOD MONITORING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

"""
        
        # Add alert summary
        alert_summary = self.generate_alert_report()
        report += alert_summary + "\n\n"
        
        # Add detailed analysis
        detailed_summary = self.summarize_flood_situation(24, "detailed")
        report += "📈 DETAILED ANALYSIS:\n" + detailed_summary + "\n\n"
        
        # Add system info
        data_summary = self.get_flood_data_summary(24)
        if "error" not in data_summary:
            report += f"""🔧 SYSTEM STATUS:
- Monitoring zones: {len(data_summary['zones'])}
- Total readings (24h): {data_summary['database_readings']}
- Data sources: Database + Google Sheets
- AI assistant: Active

🔗 ACCESS LINKS:
- Frontend Dashboard: http://localhost:8501
- API Documentation: http://localhost:8000/docs
- Backend Status: http://localhost:8000

⚡ NEXT ACTIONS:
- Monitor critical zones closely
- Update thresholds if needed
- Check sensor connectivity
- Review Google Sheets sync

Generated by AI-Powered Flood Detection System 🤖
"""
        
        return report
    
    def save_report(self, report: str, filename: Optional[str] = None) -> str:
        """Save report to file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"flood_report_{timestamp}.txt"
        
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath


#testing with hardcoded text
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Flood Detection Summarizer')
    parser.add_argument('--mode', choices=['text', 'flood', 'alerts', 'daily'], 
                       default='flood', help='Type of summary to generate')
    parser.add_argument('--hours', type=int, default=24, 
                       help='Number of hours to analyze for flood data')
    parser.add_argument('--style', choices=['concise', 'detailed', 'bullet points'], 
                       default='detailed', help='Summary style')
    parser.add_argument('--save', action='store_true', 
                       help='Save report to file')
    parser.add_argument('--text', type=str, 
                       help='Text to summarize (for text mode)')
    
    args = parser.parse_args()
    
    summarizer = Summarizer()
    
    if args.mode == 'text':
        if args.text:
            result = summarizer.summarize(args.text, args.style)
        else:
            # Use sample text for demo
            sample_text = """
            Water levels in the river rose by 2.3 meters in the last 12 hours,
            affecting three nearby villages. Evacuation centers have been set up,
            but heavy rainfall is expected to continue for the next 24 hours.
            """
            print("📝 Using sample text for demo...")
            result = summarizer.summarize(sample_text, args.style)
            
    elif args.mode == 'flood':
        result = summarizer.summarize_flood_situation(args.hours, args.style)
        
    elif args.mode == 'alerts':
        result = summarizer.generate_alert_report()
        
    elif args.mode == 'daily':
        result = summarizer.generate_daily_report()
    
    print("🌊 FLOOD DETECTION SUMMARIZER")
    print("=" * 50)
    print(result)
    
    if args.save:
        filepath = summarizer.save_report(result)
        print(f"\n💾 Report saved to: {filepath}")
    
    # Cleanup
    if hasattr(summarizer, 'db') and summarizer.db:
        summarizer.db.close()

##########################################
# unused code for reference. Ignore for now
##########################################

# import google.generativeai as genai

# # Gemini API key
# API_KEY = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"

# def summarize_text(text, system_prompt="You are a summarization assistant. Summarize clearly and concisely."):
#     try:
#         # Put system prompt inline with user content
#         response = get_model.generate_content(
#             f"{system_prompt}\n\nSummarize this:\n{text}"
#         )
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

# if __name__ == "__main__":
#     long_text = """
#     Heavy rainfall in the northern region has caused rivers to overflow. 
#     Authorities reported that water levels rose by 3 meters in 12 hours, 
#     forcing the evacuation of more than 500 families. Rescue operations 
#     are ongoing, and temporary shelters have been set up in schools and 
#     community centers. Meteorological departments have issued warnings 
#     of continued rainfall over the next 48 hours.
#     """
    
#     summary = summarize_text(long_text)
#     print("Summary:\n", summary)
