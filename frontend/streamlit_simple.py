import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time

# Page Configuration
st.set_page_config(
    page_title="🌊 Flood Detection System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL Backend API
BACKEND_URL = "http://127.0.0.1:8000"

# CSS for UI styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        border-radius: 10px;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        border-radius: 10px;
    }
    .alert-low {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_sensor_data():
    """Get sensor data from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/sensors/data", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def send_chat_message(message):
    """Send message to chatbot"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/",
            json={"prompt": message},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("reply", "No answer")
        return "Chatbot connection error"
    except:
        return "Unable to connect to chatbot. Please check the backend."

def generate_mock_data():
    """Generate mock data for demo"""
    import random
    from datetime import datetime, timedelta
    
    data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(24):
        timestamp = base_time + timedelta(hours=i)
        water_level = round(random.uniform(0.5, 3.0), 2)
        temperature = round(random.uniform(20, 35), 1)
        humidity = round(random.uniform(60, 90), 1)
        
        data.append({
            "id": i + 1,
            "water_level": water_level,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "location": f"Sensor {(i % 3) + 1}"
        })
    
    return data

def get_alert_level(water_level):
    """Determine alert level"""
    if water_level >= 2.5:
        return "Dangerous", "🔴", "alert-high"
    elif water_level >= 1.8:
        return "Warning", "🟡", "alert-medium"
    else:
        return "Safe", "🟢", "alert-low"

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🌊 IoT Flood Detection System</h1>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("🎛️ Control")

    # Check backend
    backend_status = check_backend_status()
    if backend_status:
        st.sidebar.success("✅ Backend is running")
    else:
        st.sidebar.error("❌ Backend is not running")

    # Main menu
    page = st.sidebar.selectbox(
        "Choose function:",
        ["📊 Dashboard", "🤖 Chatbot", "📈 Charts", "⚙️ Settings"]
    )
    
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🤖 Chatbot":
        show_chatbot()
    elif page == "📈 Charts":
        show_charts()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Display main dashboard"""
    st.subheader("📊 Dashboard Overview")

    # Get data (try from backend, if not available use mock data)
    sensor_data = get_sensor_data()
    if not sensor_data:
        sensor_data = generate_mock_data()
    
    if sensor_data:
        # Get latest data
        latest_data = sensor_data[-1] if sensor_data else {}
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            water_level = latest_data.get('water_level', 0)
            alert_text, alert_icon, alert_class = get_alert_level(water_level)
            st.metric(
                label="🌊 Current Water Level", 
                value=f"{water_level}m",
                delta=f"{alert_icon} {alert_text}"
            )
        
        with col2:
            temp = latest_data.get('temperature', 0)
            st.metric(
                label="🌡️ Temperature", 
                value=f"{temp}°C"
            )
        
        with col3:
            humidity = latest_data.get('humidity', 0)
            st.metric(
                label="💧 Humidity", 
                value=f"{humidity}%"
            )
        
        with col4:
            st.metric(
                label="📍 Active Sensors", 
                value="3/3",
                delta="✅ All online"
            )

        # Alert status
        st.subheader("⚠️ Alert Status")
        alert_text, alert_icon, alert_class = get_alert_level(water_level)
        
        alert_html = f"""
        <div class="{alert_class}">
            <h3>{alert_icon} Alert Level: {alert_text}</h3>
            <p>Current Water Level: <strong>{water_level}m</strong></p>
            <p>Last Updated: <strong>{latest_data.get('timestamp', 'N/A')}</strong></p>
        </div>
        """
        st.markdown(alert_html, unsafe_allow_html=True)

        # Recent sensor data table
        st.subheader("📋 Recent Sensor Data")
        df = pd.DataFrame(sensor_data[-10:])  # 10 most recent rows
        st.dataframe(df, use_container_width=True)
        
    else:
        st.warning("⚠️ No sensor data available")

def show_chatbot():
    """Display chatbot interface"""
    st.subheader("🤖 AI Flood Support Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm the AI assistant for the flood monitoring system. You can ask me about water levels, alerts, or flood prevention measures."}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = send_chat_message(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat history button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared. What new questions do you have?"}
        ]
        st.rerun()

def show_charts():
    """Display charts and analysis"""
    st.subheader("� Charts and Analysis")

    # Get data
    sensor_data = get_sensor_data()
    if not sensor_data:
        sensor_data = generate_mock_data()
    
    if sensor_data:
        df = pd.DataFrame(sensor_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Water Level Chart
        st.subheader("🌊 Water Level Chart (Last 24h)")
        st.line_chart(df.set_index('timestamp')['water_level'])
        st.info("🔴 Dangerous: > 2.5m | 🟡 Warning: > 1.8m | 🟢 Safe: < 1.8m")

        # Temperature and Humidity Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌡️ Temperature")
            st.line_chart(df.set_index('timestamp')['temperature'])
        
        with col2:
            st.subheader("💧 Humidity")
            st.line_chart(df.set_index('timestamp')['humidity'])

        # Statistics
        st.subheader("📊 Overview Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"🌊 Average Water Level: {df['water_level'].mean():.2f}m")
        with col2:
            st.info(f"🌡️ Average Temperature: {df['temperature'].mean():.1f}°C")
        with col3:
            st.info(f"💧 Average Humidity: {df['humidity'].mean():.1f}%")

def show_settings():
    """Display system settings"""
    st.subheader("⚙️ System Settings")

    st.markdown("### 🔧 Backend Configuration")
    new_backend_url = st.text_input("Backend URL:", value=BACKEND_URL)

    if st.button("🧪 Test Connection"):
        try:
            response = requests.get(f"{new_backend_url}/", timeout=5)
            if response.status_code == 200:
                st.success("✅ Connection successful!")
                st.json(response.json())
            else:
                st.error(f"❌ Connection error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Unable to connect: {str(e)}")

    st.markdown("### 📋 System Information")
    st.info("""
    **Version:** 1.0.0  
    **Technology:** Python + Streamlit + FastAPI  
    **Author:** GPBL Team  
    **Description:** IoT Flood monitoring system using AI
    """)

if __name__ == "__main__":
    main()
