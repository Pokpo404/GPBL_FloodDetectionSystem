import google.generativeai as genai

# Gemini API key
GEMINI_API_KEY = "AIzaSyDg8T9a1FzYeA2JGWgTeUKCn7y4CAv_mM0"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Reusable model instance
model = genai.GenerativeModel("gemini-1.5-pro")

def get_model():
    genai.configure(api_key=GEMINI_API_KEY)
    return "gemini-1.5-pro"

def generate(prompt: str, max_tokens: int = 256) -> str:
    """
    Generate response using Gemini AI
    """
    try:
        # Check if it's a greeting
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'chào', 'xin chào']
        if any(greeting in prompt.lower() for greeting in greetings):
            return """Hi there! Welcome to the Flood Detection System! 

I'm your AI assistant here to help with flood monitoring and safety information. I can help you with:

• Current water levels and flood alerts
• Sensor data from monitoring zones  
• Emergency guidance and safety recommendations
• Flood risk assessments and predictions
• Real-time alerts and status updates

What would you like to know about the flood situation? Just ask me anything!"""
        
        # Create system prompt for flood support
        system_prompt = """You are an AI assistant specialized in flood support and disaster management. 
        Please provide short, helpful and relevant answers about:
        - Water level information and flood alerts
        - Disaster prevention measures
        - Safety instructions during floods
        - Weather and environmental forecasts
        
        Respond in English and be friendly and professional."""
        
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I encountered an error while processing: {str(e)}"

def generate_with_context(prompt: str, sensor_context: str, max_tokens: int = 256) -> str:
    """
    Generate response using Gemini AI with sensor data context
    """
    try:
        # Check if it's a greeting first
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'chào', 'xin chào']
        if any(greeting in prompt.lower() for greeting in greetings):
            # Get current alert summary from sensor context
            critical_count = sensor_context.count('critical')
            warning_count = sensor_context.count('warning')
            
            alert_summary = ""
            if critical_count > 0:
                alert_summary = f"\n[ALERT] {critical_count} critical flood warnings detected!"
            elif warning_count > 0:
                alert_summary = f"\n[CAUTION] {warning_count} flood warnings active."
            else:
                alert_summary = "\n[STATUS] All zones reporting normal levels."
            
            return f"""Hi there! Welcome to the Flood Detection System! 

I'm your AI assistant monitoring flood conditions in real-time. Here's the current situation:
{alert_summary}

I can help you with:
• Current water levels at all monitoring zones
• Real-time sensor data analysis  
• Emergency alerts and safety guidance
• Zone-specific flood risk assessments
• Trends and predictions
• Data validation and system status

What would you like to know about the flood situation? I have access to live sensor data!"""
        
        # Create enhanced system prompt with sensor data
        system_prompt = f"""You are an AI assistant for a flood monitoring system. 
        You have access to real-time sensor data from multiple sources and should use this information to provide accurate, data-driven responses.
        
        {sensor_context}
        
        IMPORTANT GUIDELINES:
        - If you detect data discrepancies between sources, clearly explain the difference and provide safety-first recommendations
        - Always specify data sources (Database vs Google Sheets) when mentioning readings
        - For conflicting data, recommend the more conservative (higher risk) interpretation for safety
        - Provide specific timestamps and locations when available
        - Include actionable next steps for authorities and residents
        
        Based on this sensor data, please provide helpful answers about:
        - Current water levels and flood risk assessment with source attribution
        - Alert status and safety recommendations prioritizing public safety
        - Data discrepancy analysis and recommended actions
        - Emergency guidance based on current conditions
        - System reliability and data validation status
        
        Always reference the actual sensor data when relevant. Be professional, precise, and prioritize safety."""
        
        full_prompt = f"{system_prompt}\n\nUser question: {prompt}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"Sorry, I encountered an error while processing: {str(e)}"