# backend/services/google_sheets_service.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any, Optional
import os
import datetime

def _try_parse_ts(ts_str: str) -> Optional[datetime.datetime]:
    if not ts_str:
        return None
    s = str(ts_str).strip()
    fmts = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y-%m-%d")
    for f in fmts:
        try:
            return datetime.datetime.strptime(s, f)
        except Exception:
            pass
    # fallback to dateutil if available
    try:
        from dateutil import parser as _p
        return _p.parse(s)
    except Exception:
        return None

class GoogleSheetsService:
    def __init__(
        self,
        credentials_file: str = "config/credentials.json",
        spreadsheet_id: Optional[str] = None,
        sheet_name: Optional[str] = None,
        allowed_device: Optional[str] = "waterlevel"
    ):
        self.credentials_file = credentials_file
        self.spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
        self.sheet_name = sheet_name or os.getenv("SHEET_NAME", "Sheet1")
        self.allowed_device = allowed_device
        self.client = None
        self.spreadsheet = None
        self._authenticate()

    def _authenticate(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        if not os.path.exists(self.credentials_file):
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        self.client = gspread.authorize(credentials)
        if self.spreadsheet_id:
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        else:
            ss_name = os.getenv("SPREADSHEET_NAME")
            if ss_name:
                self.spreadsheet = self.client.open(ss_name)
            else:
                try:
                    self.spreadsheet = self.client.openall()[0]
                except Exception:
                    self.spreadsheet = None

    def _parse_row_using_header(self, header: List[str], row: List[str]) -> Optional[Dict[str, Any]]:
        hdr_map = {h.strip().lower(): i for i, h in enumerate(header)}
        expected = ["timestamp", "device_id", "distance_cm"]
        if not all(k in hdr_map for k in expected):
            return None
        try:
            ts_raw = row[hdr_map["timestamp"]] if len(row) > hdr_map["timestamp"] else ""
            device_raw = row[hdr_map["device_id"]] if len(row) > hdr_map["device_id"] else ""
            dist_raw = row[hdr_map["distance_cm"]] if len(row) > hdr_map["distance_cm"] else ""

            ts = _try_parse_ts(ts_raw)
            device = device_raw.strip()
            try:
                distance_cm = float(dist_raw) if str(dist_raw).strip() != "" else None
            except Exception:
                return None

            return {"timestamp": ts, "device_id": device, "water_level": distance_cm}
        except Exception:
            return None

    def get_sensor_data(self, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            if not self.spreadsheet:
                raise RuntimeError("No spreadsheet opened. Check SPREADSHEET_ID or permissions.")

            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            all_values = worksheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []

            header = all_values[0]
            rows = all_values[1:limit+1] if limit else all_values[1:]

            sensor_data = []
            for r in rows:
                parsed = self._parse_row_using_header(header, r)
                if not parsed:
                    continue
                # require parsed timestamp and water_level
                if parsed["timestamp"] is None or parsed["water_level"] is None:
                    continue
                if self.allowed_device:
                    if parsed["device_id"].lower() != self.allowed_device.lower():
                        continue
                # compute status with thresholds (distance small -> critical)
                parsed["status"] = self._get_status(parsed["water_level"])
                sensor_data.append(parsed)

            return sensor_data
        except Exception as e:
            print(f"[GoogleSheetsService] Failed to get sensor data: {e}")
            return []

    def get_latest_sensor_data(self) -> Optional[Dict[str, Any]]:
        try:
            data = self.get_sensor_data(limit=1)
            return data[0] if data else None
        except Exception as e:
            print(f"Failed to get latest sensor data: {str(e)}")
            return None

    def _get_status(self, water_level: float) -> str:
        warning_threshold = float(os.getenv("WARNING_THRESHOLD_CM", "50"))
        critical_threshold = float(os.getenv("CRITICAL_THRESHOLD_CM", "20"))
        # smaller distance => water is closer to sensor => more critical
        if water_level > warning_threshold:
            return "normal"
        elif water_level > critical_threshold:
            return "warning"
        else:
            return "critical"
