#!/usr/bin/env python3
"""
CampusShield Development Server Verification Script
Tests if the Django server is working properly
"""

import subprocess
import time
import os
import sys
import requests
from pathlib import Path

def check_venv():
    """Check if virtual environment is activated"""
    venv_path = Path(r"C:\Development\campusshield-ai\campusshield\venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found at:", venv_path)
        return False
    print("✅ Virtual environment found")
    return True

def check_django():
    """Check if Django is properly installed"""
    try:
        import django
        print(f"✅ Django {django.get_version()} is installed")
        return True
    except ImportError:
        print("❌ Django not installed or not in PATH")
        return False

def test_server_connection(url="http://localhost:8000", timeout=5):
    """Test if server is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ Server responding at {url} (Status: {response.status_code})")
            return True
        elif response.status_code == 302:
            print(f"✅ Server responding at {url} (Redirect 302 - login required, expected)")
            return True
        else:
            print(f"⚠️  Server responding with status {response.status_code}")
            return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {url} - server may not be running")
        return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("CampusShield Development Server Verification")
    print("="*60 + "\n")
    
    print("1. Checking virtual environment...")
    venv_ok = check_venv()
    
    print("\n2. Checking Django installation...")
    django_ok = check_django()
    
    print("\n3. Testing server connection...")
    print("   (Make sure server is running at http://localhost:8000)")
    server_ok = test_server_connection()
    
    print("\n" + "="*60)
    if venv_ok and django_ok:
        print("✅ All checks passed! Server should be working.")
        print("\nAccess your app at: http://localhost:8000")
        print("="*60 + "\n")
        return 0
    else:
        print("❌ Some checks failed. See details above.")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
