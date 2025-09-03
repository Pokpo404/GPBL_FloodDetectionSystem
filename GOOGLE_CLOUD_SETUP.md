# 🔐 Google Sheets API Setup Guide

## Step 1: Create Google Cloud Project & Enable API

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create New Project** (or use existing):
   - Click "Select a project" → "New Project"
   - Name: `Flood Detection System`
   - Click "Create"

3. **Enable Google Sheets API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

## Step 2: Create Service Account

1. **Navigate to Service Accounts**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"

2. **Configure Service Account**:
   - Service account name: `flood-detection-bot`
   - Service account ID: `flood-detection-bot` (auto-filled)
   - Description: `Service account for flood detection system`
   - Click "Create and Continue"

3. **Set Permissions** (Optional):
   - Skip this step for now
   - Click "Continue" → "Done"

## Step 3: Generate Credentials JSON

1. **Create Key**:
   - Click on your new service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Select "JSON"
   - Click "Create"

2. **Download & Install**:
   - Save the downloaded JSON file as `credentials.json`
   - Move it to your project: `config/credentials.json`

## Step 4: Share Google Sheet with Service Account

1. **Get Service Account Email**:
   - From the downloaded JSON file, copy the `client_email` field
   - It looks like: `flood-detection-bot@your-project-id.iam.gserviceaccount.com`

2. **Share Your Google Sheet**:
   - Open your Google Sheet: https://docs.google.com/spreadsheets/d/1fbo49WGPzdh4YACQ7VdjZIpiBvblLhKlvzdmHJYcQwY/edit#gid=1231782873
   - Click "Share" button (top-right)
   - Add the service account email
   - Set permission to "Editor"
   - Uncheck "Notify people"
   - Click "Share"

## Step 5: Verify Setup

Run the test script to verify everything works:
```bash
python test_google_sheets.py
```

## Sample credentials.json Structure

Your `config/credentials.json` should look like this:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "flood-detection-bot@your-project-id.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/flood-detection-bot%40your-project-id.iam.gserviceaccount.com"
}
```

## Troubleshooting

### Error: "File not found"
- Make sure `credentials.json` is in the `config/` folder
- Check file permissions

### Error: "Permission denied"
- Verify you shared the sheet with the service account email
- Make sure the service account has "Editor" permissions

### Error: "API not enabled"
- Enable Google Sheets API in Google Cloud Console
- Wait a few minutes for changes to propagate

## Security Notes

- ⚠️ **Never commit credentials.json to git**
- Add `config/credentials.json` to your `.gitignore`
- Keep your service account key secure
- Consider using environment variables for production
