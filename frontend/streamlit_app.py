import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time

# Import plotly với điều kiện
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    go = None

# Cấu hình trang
st.set_page_config(
    page_title="Flood Detection System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL Backend API
BACKEND_URL = "http://127.0.0.1:8000"

# CSS để làm đẹp giao diện
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
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
    """Kiểm tra backend có hoạt động không"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_sensor_data():
    """Lấy dữ liệu cảm biến từ backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/sensors/data", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def send_chat_message(message):
    """Gửi tin nhắn tới chatbot"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/",
            json={"prompt": message},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("reply", "Không có phản hồi")
        return "Lỗi kết nối chatbot"
    except:
        return "Không thể kết nối tới chatbot. Vui lòng kiểm tra backend."

def generate_mock_data():
    """Tạo dữ liệu giả để demo"""
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
            "location": f"Cảm biến {(i % 3) + 1}"
        })
    
    return data

def get_alert_level(water_level):
    """Xác định mức độ cảnh báo"""
    if water_level >= 2.5:
        return "Nguy hiểm", "🔴", "alert-high"
    elif water_level >= 1.8:
        return "Cảnh báo", "🟡", "alert-medium"
    else:
        return "An toàn", "🟢", "alert-low"

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">Hệ thống Giám sát Lũ lụt IoT</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title(" Điều khiển")
    
    # Kiểm tra backend
    backend_status = check_backend_status()
    if backend_status:
        st.sidebar.success(" Backend đang hoạt động")
    else:
        st.sidebar.error(" Backend không hoạt động")
    
    # Menu chính
    page = st.sidebar.selectbox(
        "Chọn chức năng:",
        ["Dashboard", "Chatbot", " Biểu đồ", "Cài đặt"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Chatbot":
        show_chatbot()
    elif page == "Biểu đồ":
        show_charts()
    elif page == "Cài đặt":
        show_settings()

def show_dashboard():
    """Hiển thị dashboard chính"""
    st.subheader("Bảng điều khiển tổng quan")
    
    # Lấy dữ liệu (thử từ backend, nếu không có thì dùng mock data)
    sensor_data = get_sensor_data()
    if not sensor_data:
        sensor_data = generate_mock_data()
    
    if sensor_data:
        # Lấy dữ liệu mới nhất
        latest_data = sensor_data[-1] if sensor_data else {}
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            water_level = latest_data.get('water_level', 0)
            alert_text, alert_icon, alert_class = get_alert_level(water_level)
            st.metric(
                label="Mực nước hiện tại", 
                value=f"{water_level}m",
                delta=f"{alert_icon} {alert_text}"
            )
        
        with col2:
            temp = latest_data.get('temperature', 0)
            st.metric(
                label="Nhiệt độ", 
                value=f"{temp}°C"
            )
        
        with col3:
            humidity = latest_data.get('humidity', 0)
            st.metric(
                label="Độ ẩm", 
                value=f"{humidity}%"
            )
        
        with col4:
            st.metric(
                label="Cảm biến hoạt động", 
                value="3/3",
                delta="Tất cả online"
            )
        
        # Cảnh báo
        st.subheader("Tình trạng cảnh báo")
        alert_text, alert_icon, alert_class = get_alert_level(water_level)
        
        alert_html = f"""
        <div class="{alert_class}">
            <h3>{alert_icon} Mức cảnh báo: {alert_text}</h3>
            <p>Mực nước hiện tại: <strong>{water_level}m</strong></p>
            <p>Thời gian cập nhật: <strong>{latest_data.get('timestamp', 'N/A')}</strong></p>
        </div>
        """
        st.markdown(alert_html, unsafe_allow_html=True)
        
        # Bảng dữ liệu gần đây
        st.subheader("Dữ liệu cảm biến gần đây")
        df = pd.DataFrame(sensor_data[-10:])  # 10 dòng gần nhất
        st.dataframe(df, use_container_width=True)
        
    else:
        st.warning("Không có dữ liệu cảm biến")

def show_chatbot():
    """Hiển thị chatbot"""
    st.subheader("Trợ lý AI Flood Support")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Xin chào! Tôi là trợ lý AI cho hệ thống giám sát lũ lụt. Bạn có thể hỏi tôi về tình hình mực nước, cảnh báo, hoặc các biện pháp phòng chống lũ lụt."}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Đang xử lý..."):
                response = send_chat_message(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Nút xóa lịch sử chat
    if st.button(" Xóa lịch sử chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Lịch sử chat đã được xóa. Bạn có câu hỏi gì mới?"}
        ]
        st.rerun()

def show_charts():
    """Hiển thị biểu đồ"""
    st.subheader("Biểu đồ và Phân tích")
    
    # Lấy dữ liệu
    sensor_data = get_sensor_data()
    if not sensor_data:
        sensor_data = generate_mock_data()
    
    if sensor_data:
        df = pd.DataFrame(sensor_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Biểu đồ mực nước theo thời gian
        st.subheader("🌊 Biểu đồ mực nước 24h")
        if PLOTLY_AVAILABLE:
            fig_water = px.line(
                df, 
                x='timestamp', 
                y='water_level',
                title='Mực nước theo thời gian',
                labels={'water_level': 'Mực nước (m)', 'timestamp': 'Thời gian'}
            )
            fig_water.add_hline(y=2.5, line_dash="dash", line_color="red", 
                               annotation_text="Nguy hiểm")
            fig_water.add_hline(y=1.8, line_dash="dash", line_color="orange", 
                               annotation_text="Cảnh báo")
            st.plotly_chart(fig_water, use_container_width=True)
        else:
            # Fallback: Sử dụng line_chart của Streamlit
            st.line_chart(df.set_index('timestamp')['water_level'])
            st.info("🔴 Nguy hiểm: > 2.5m | 🟡 Cảnh báo: > 1.8m | 🟢 An toàn: < 1.8m")
        
        # Biểu đồ nhiệt độ và độ ẩm
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌡️ Nhiệt độ")
            if PLOTLY_AVAILABLE:
                fig_temp = px.line(df, x='timestamp', y='temperature', 
                                 title='Nhiệt độ theo thời gian')
                st.plotly_chart(fig_temp, use_container_width=True)
            else:
                st.line_chart(df.set_index('timestamp')['temperature'])
        
        with col2:
            st.subheader("💧 Độ ẩm")
            if PLOTLY_AVAILABLE:
                fig_humidity = px.line(df, x='timestamp', y='humidity', 
                                     title='Độ ẩm theo thời gian')
                st.plotly_chart(fig_humidity, use_container_width=True)
            else:
                st.line_chart(df.set_index('timestamp')['humidity'])
        
        # Thống kê
        st.subheader("📊 Thống kê tổng quan")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"🌊 Mực nước trung bình: {df['water_level'].mean():.2f}m")
        with col2:
            st.info(f"🌡️ Nhiệt độ trung bình: {df['temperature'].mean():.1f}°C")
        with col3:
            st.info(f"💧 Độ ẩm trung bình: {df['humidity'].mean():.1f}%")

def show_settings():
    """Hiển thị cài đặt"""
    st.subheader("Cài đặt hệ thống")
    
    st.markdown("### Cấu hình Backend")
    new_backend_url = st.text_input("URL Backend:", value=BACKEND_URL)
    
    if st.button("Test kết nối"):
        try:
            response = requests.get(f"{new_backend_url}/", timeout=5)
            if response.status_code == 200:
                st.success(" Kết nối thành công!")
                st.json(response.json())
            else:
                st.error(f"Lỗi kết nối: {response.status_code}")
        except Exception as e:
            st.error(f"Không thể kết nối: {str(e)}")
    
    st.markdown("### Thông tin hệ thống")
    st.info("""
    **Phiên bản:** 1.0.0  
    **Công nghệ:** Python + Streamlit + FastAPI  
    **Tác giả:** GPBL Team  
    **Mô tả:** Hệ thống giám sát lũ lụt sử dụng IoT và AI
    """)

if __name__ == "__main__":
    main()
