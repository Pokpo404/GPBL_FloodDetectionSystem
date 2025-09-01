#!/usr/bin/env python3
"""
🚀 Flood Detection System - Quick Start Script
Chạy hệ thống phát hiện lũ lụt với IoT và AI
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8+ để chạy hệ thống")
        print(f"   Phiên bản hiện tại: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - OK")

def check_dependencies():
    """Kiểm tra dependencies"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        print("✅ Dependencies đã cài đặt")
        return True
    except ImportError as e:
        print(f"❌ Thiếu dependency: {e}")
        print("📦 Chạy: pip install -r requirements.txt")
        return False

def check_config():
    """Kiểm tra cấu hình"""
    config_dir = Path("config")
    env_file = config_dir / ".env"
    credentials_file = config_dir / "credentials.json"
    
    if not env_file.exists():
        print("⚠️  File .env chưa tạo")
        print("📝 Copy: cp config/env_example.txt config/.env")
        print("📝 Cập nhật GOOGLE_SPREADSHEET_ID trong file .env")
    
    if not credentials_file.exists():
        print("⚠️  File credentials.json chưa tạo")
        print("🔑 Tạo Google Sheets API credentials")
        print("📁 Lưu vào: config/credentials.json")
    
    return env_file.exists() and credentials_file.exists()

def run_system():
    """Chạy hệ thống"""
    print("\n🚀 Khởi động Flood Detection System...")
    
    # Chuyển đến thư mục backend
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Không tìm thấy thư mục backend")
        sys.exit(1)
    
    os.chdir(backend_dir)
    
    # Chạy hệ thống
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Dừng hệ thống...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy hệ thống: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("🌊 Flood Detection System - Quick Start")
    print("=" * 50)
    
    # Kiểm tra Python version
    check_python_version()
    
    # Kiểm tra dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Kiểm tra cấu hình
    if not check_config():
        print("\n⚠️  Vui lòng cấu hình trước khi chạy")
        print("📖 Xem hướng dẫn: QUICK_START.md")
        response = input("\n🤔 Vẫn muốn chạy? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Chạy hệ thống
    run_system()

if __name__ == "__main__":
    main()
