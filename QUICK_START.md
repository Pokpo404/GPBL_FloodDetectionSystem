# 🚀 Flood Detection System - Quick Start

## 📋 Yêu cầu
- Python 3.8+
- Google Sheets API credentials

## ⚡ Chạy nhanh

### **Bước 1: Cài đặt**
```bash
pip install -r requirements.txt
```

### **Bước 2: Cấu hình Google Sheets**
1. Tạo file `config/credentials.json` với Google Sheets API credentials
2. Copy `config/env_example.txt` → `config/.env`
3. Cập nhật `GOOGLE_SPREADSHEET_ID` trong file `.env`

### **Bước 3: Chạy hệ thống**
```bash
cd backend
python main.py
```

## 🌐 API Endpoints
- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 📡 Test API

### **Thêm sensor data**
```bash
curl -X POST "http://localhost:8000/api/v1/sensors/" \
  -H "Content-Type: application/json" \
  -d '{"water_level": 45.5, "device_id": "sensor_001"}'
```

### **Lấy IoT data**
```bash
curl "http://localhost:8000/api/v1/sensors/iot"
```

### **Chat với AI**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Mực nước hiện tại là bao nhiêu?"}'
```

## 🔧 Google Sheets Setup

### **1. Tạo Service Account**
1. Vào [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project → Enable Google Sheets API
3. Tạo Service Account → Download JSON
4. Đổi tên thành `credentials.json` → Copy vào `config/`

### **2. Chia sẻ Google Sheets**
1. Mở Google Sheets của bạn
2. Click "Share" → Thêm email của Service Account
3. Cấp quyền "Editor"

### **3. Cấu hình Environment**
```bash
cp config/env_example.txt config/.env
# Cập nhật GOOGLE_SPREADSHEET_ID trong file .env
```

## 📊 Cấu trúc dữ liệu IoT
- **Column A**: timestamp_iso
- **Column C**: device_id  
- **Column E**: level_mm (mực nước mm)
- **Column F**: wet (trạng thái ướt)

## 🎯 Tính năng
- ✅ Thêm/lấy dữ liệu sensor
- ✅ Đọc dữ liệu IoT từ Google Sheets
- ✅ Chat với AI về mực nước
- ✅ Thống kê dữ liệu

## 🐛 Troubleshooting

### **Lỗi Google Sheets**
```bash
ls config/credentials.json
cat config/.env
```

### **Lỗi Database**
```bash
rm backend/flood_detection.db
python main.py
```

### **Lỗi Port**
```bash
export PORT=8080
python main.py
```
