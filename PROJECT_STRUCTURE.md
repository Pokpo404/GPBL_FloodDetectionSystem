# Cấu trúc Folder - Hệ thống Phát hiện Lũ lụt

```
GPBL_FloodDetectionSystem/
│
├── 📁 backend/                          # Backend API Server
│   ├── 📄 __init__.py
│   ├── 📄 main.py                       # FastAPI application
│   ├── 📄 models.py                     # SQLAlchemy database models
│   ├── 📄 schemas.py                    # Pydantic schemas
│   ├── 📄 database.py                   # Database operations & CRUD
│   ├── 📄 config.py                     # Configuration settings
│   │
│   ├── 📁 api/                          # API routes
│   │   ├── 📄 __init__.py
│   │   ├── 📄 sensors.py                # Sensor endpoints
│   │   ├── 📄 chat.py                   # Chat endpoints
│   │   └── 📄 analysis.py               # Analysis endpoints
│   │
│   ├── 📁 services/                     # Business logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 sensor_service.py         # Sensor data processing
│   │   ├── 📄 chat_service.py           # Chat/LLM processing
│   │   ├── 📄 google_sheets_service.py  # Google Sheets integration
│   │   └── 📄 analysis_service.py       # Data analysis & predictions
│   │
│   ├── 📁 utils/                        # Utility functions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 helpers.py                # Helper functions
│   │   ├── 📄 validators.py             # Data validation
│   │   └── 📄 constants.py              # Constants & thresholds
│   │
│   └── 📁 tests/                        # Unit tests
│       ├── 📄 __init__.py
│       ├── 📄 test_sensors.py
│       ├── 📄 test_chat.py
│       └── 📄 test_analysis.py
│
├── 📁 frontend/                         # Frontend (nếu cần)
│   ├── 📄 index.html
│   ├── 📄 style.css
│   └── 📄 script.js
│
├── 📁 data/                             # Data storage
│   ├── 📄 flood_detection.db            # SQLite database
│   ├── 📄 sensor_data.csv               # CSV backup
│   └── 📄 chat_history.json             # Chat backup
│
├── 📁 config/                           # Configuration files
│   ├── 📄 credentials.json              # Google Sheets credentials
│   ├── 📄 .env                          # Environment variables
│   └── 📄 settings.json                 # Application settings
│
├── 📁 docs/                             # Documentation
│   ├── 📄 API_DOCUMENTATION.md
│   ├── 📄 SETUP_GUIDE.md
│   └── 📄 DEPLOYMENT.md
│
├── 📁 scripts/                          # Utility scripts
│   ├── 📄 setup_database.py             # Database initialization
│   ├── 📄 import_data.py                # Data import script
│   └── 📄 backup_data.py                # Data backup script
│
├── 📄 requirements.txt                  # Python dependencies
├── 📄 README.md                         # Project overview
├── 📄 .gitignore                        # Git ignore rules
├── 📄 .env.example                      # Environment variables template
└── 📄 PROJECT_STRUCTURE.md              # This file
```

## Mô tả các thành phần chính:

### 📁 backend/
- **main.py**: Entry point của FastAPI application
- **models.py**: Định nghĩa database tables (SensorData, ChatMessage)
- **schemas.py**: Pydantic models cho API requests/responses
- **database.py**: CRUD operations và database connections

### 📁 backend/api/
- **sensors.py**: Endpoints cho sensor data (/sensors)
- **chat.py**: Endpoints cho chat messages (/chat)
- **analysis.py**: Endpoints cho data analysis

### 📁 backend/services/
- **sensor_service.py**: Logic xử lý sensor data
- **chat_service.py**: Logic xử lý chat với LLM
- **google_sheets_service.py**: Tích hợp Google Sheets
- **analysis_service.py**: Phân tích dữ liệu và dự đoán

### 📁 config/
- **credentials.json**: Google Sheets API credentials
- **.env**: Environment variables (database URL, API keys)
- **settings.json**: Cấu hình ứng dụng

### 📁 data/
- **flood_detection.db**: SQLite database file
- **sensor_data.csv**: Backup dữ liệu sensor
- **chat_history.json**: Backup lịch sử chat

### 📁 scripts/
- **setup_database.py**: Script khởi tạo database
- **import_data.py**: Script import dữ liệu từ Google Sheets
- **backup_data.py**: Script backup dữ liệu

## Các file quan trọng cần tạo:

1. **backend/database.py** - CRUD operations
2. **backend/main.py** - FastAPI application
3. **backend/api/sensors.py** - Sensor endpoints
4. **backend/api/chat.py** - Chat endpoints
5. **backend/services/google_sheets_service.py** - Google Sheets integration
6. **config/.env** - Environment variables
7. **config/credentials.json** - Google Sheets credentials
