# 🔧 Google Sheets Setup Guide

## ❌ Current Issues Found:
1. **credentials.json is EMPTY** (0 bytes) 
2. **Spreadsheet ID might be incomplete**
3. **Missing proper Google Sheets authentication**

## ✅ How to Fix:

### Step 1: Get Google Sheets Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Sheets API** and **Google Drive API**
4. Create **Service Account** credentials
5. Download the JSON key file
6. Replace content in `config/credentials.json`

### Step 2: Verify Spreadsheet ID
Current ID: `1fbo49WGPzdh4YACQ7VdjZIpiBvblLhKlvzdmHJYcQwY`

**Check your Google Sheets URL:**
```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
```

**Example:**
```
https://docs.google.com/spreadsheets/d/1fbo49WGPzdh4YACQ7VdjZIpiBvblLhKlvzdmHJYcQwY/edit
```

### Step 3: Share Spreadsheet
1. Open your Google Sheets
2. Click **Share** button
3. Add the **service account email** from credentials.json
4. Give **Editor** permissions

### Step 4: Verify Sheet Structure
Your sheet should have columns:
- **device_id** (e.g., SENSOR_001)
- **water_level** (numeric)
- **location** (text)
- **status** (normal/warning/critical)
- **timestamp** (datetime)

## 🧪 Test Google Sheets Connection:

```python
# Run this to test:
python -c "
from backend.services.google_sheets_service import GoogleSheetsService
try:
    gs = GoogleSheetsService()
    print('✅ Google Sheets connection successful!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

## 📋 Example credentials.json format:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service@your-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

---
**After completing these steps, restart your backend and test again!** 🚀
