# 🌊 Flood Detection System

Hệ thống phát hiện lũ lụt thông minh sử dụng IoT, AI và LLM với tích hợp Google Sheets.

## 🚀 Tính năng chính

- **📊 Monitoring**: Theo dõi mực nước real-time
- **🤖 AI Chat**: Trợ lý AI thông minh
- **📈 Analytics**: Phân tích dữ liệu và xu hướng
- **📋 Google Sheets**: Tích hợp với Google Sheets
- **🔔 Alerts**: Cảnh báo tự động
- **📱 API**: RESTful API hoàn chỉnh

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Water Level   │    │   FastAPI       │    │   Google        │
│   Sensor        │───▶│   Backend       │───▶│   Sheets        │
│   (IoT)         │    │   (SQLite)      │    │   Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AI Chat       │
                       │   Interface     │
                       │   (LLM)         │
                       └─────────────────┘
```

## 📋 Yêu cầu hệ thống

- Python 3.8+
- SQLite
- Google Sheets API (tùy chọn)

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd GPBL_FloodDetectionSystem
```

### 2. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment
```bash
# Copy file mẫu
cp config/env_example.txt config/.env

# Chỉnh sửa file .env với thông tin của bạn
nano config/.env
```

### 5. Khởi tạo database
```bash
python scripts/setup_database.py
```

### 6. Chạy ứng dụng
```bash
python backend/main.py
```

## 🔧 Cấu hình Google Sheets

### 1. Tạo Google Cloud Project
1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới
3. Enable Google Sheets API

### 2. Tạo Service Account
1. Vào "IAM & Admin" > "Service Accounts"
2. Tạo service account mới
3. Tạo key (JSON format)
4. Download file credentials

### 3. Cấu hình Spreadsheet
1. Tạo Google Spreadsheet mới
2. Share với service account email
3. Copy Spreadsheet ID từ URL

### 4. Cập nhật .env file
```env
GOOGLE_CREDENTIALS_FILE=config/credentials.json
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints chính

#### Sensors
- `POST /api/v1/sensors/` - Thêm dữ liệu sensor
- `GET /api/v1/sensors/` - Lấy danh sách sensor data
- `GET /api/v1/sensors/latest` - Lấy dữ liệu mới nhất
- `GET /api/v1/sensors/{id}` - Lấy sensor data theo ID
- `GET /api/v1/sensors/analytics/statistics` - Thống kê
- `GET /api/v1/sensors/analytics/trend` - Phân tích xu hướng

#### Chat
- `POST /api/v1/chat/` - Gửi tin nhắn và nhận phản hồi AI
- `GET /api/v1/chat/` - Lấy lịch sử chat
- `GET /api/v1/chat/session/{session_id}` - Lấy chat theo session
- `POST /api/v1/chat/session/new` - Tạo session mới

#### System
- `GET /` - Thông tin hệ thống
- `GET /health` - Kiểm tra sức khỏe hệ thống
- `GET /docs` - API Documentation (Swagger)
- `GET /redoc` - API Documentation (ReDoc)

## 💡 Sử dụng API

### Thêm dữ liệu sensor
```bash
curl -X POST "http://localhost:8000/api/v1/sensors/" \
  -H "Content-Type: application/json" \
  -d '{
    "water_level": 45.5,
    "location": "Hanoi",
    "notes": "Normal reading"
  }'
```

### Chat với AI
```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "Mực nước hiện tại là bao nhiêu?",
    "session_id": "user_session_001"
  }'
```

### Lấy thống kê
```bash
curl "http://localhost:8000/api/v1/sensors/analytics/statistics?days=7"
```

## 🗄️ Database Schema

### SensorData Table
```sql
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY,
    water_level FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100) DEFAULT 'Default Location',
    status VARCHAR(20) DEFAULT 'normal',
    notes TEXT
);
```

### ChatMessage Table
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    user_id VARCHAR(100)
);
```

## 🔍 Monitoring & Analytics

### Water Level Thresholds
- **Normal**: < 50cm
- **Warning**: 50-100cm
- **Critical**: > 100cm

### Analytics Features
- Thống kê theo thời gian
- Phân tích xu hướng
- Cảnh báo tự động
- Báo cáo chi tiết

## 🧪 Testing

### Chạy tests
```bash
pytest backend/tests/
```

### Test API endpoints
```bash
# Test health check
curl http://localhost:8000/health

# Test sensor endpoints
curl http://localhost:8000/api/v1/sensors/

# Test chat endpoints
curl http://localhost:8000/api/v1/chat/
```

## 📊 Google Sheets Integration

Hệ thống tự động đồng bộ dữ liệu với Google Sheets:

- **SensorData Sheet**: Lưu trữ dữ liệu sensor
- **ChatMessages Sheet**: Lưu trữ lịch sử chat

### Sync thủ công
```bash
# Sync sensor data
curl -X POST "http://localhost:8000/api/v1/sensors/sync-to-sheets"

# Sync chat data
curl -X POST "http://localhost:8000/api/v1/chat/sync-to-sheets"
```

## 🚀 Deployment

### Development
```bash
python backend/main.py
```

### Production
```bash
# Sử dụng Gunicorn
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Hoặc sử dụng Docker
docker build -t flood-detection-system .
docker run -p 8000:8000 flood-detection-system
```

## 🔧 Troubleshooting

### Lỗi thường gặp

1. **Database connection failed**
   - Kiểm tra file database có tồn tại không
   - Chạy lại setup script

2. **Google Sheets authentication failed**
   - Kiểm tra file credentials.json
   - Kiểm tra spreadsheet permissions
   - Verify spreadsheet ID

3. **Import errors**
   - Kiểm tra Python path
   - Cài đặt lại dependencies

### Logs
```bash
# Xem logs
tail -f logs/app.log

# Debug mode
LOG_LEVEL=DEBUG python backend/main.py
```

## 📞 Support

- **Email**: support@flooddetection.com
- **Documentation**: `/docs` endpoint
- **Issues**: GitHub Issues

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

---

**Made with ❤️ by GPBL Team** 

