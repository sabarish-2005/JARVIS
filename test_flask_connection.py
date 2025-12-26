#!/usr/bin/env python3
"""
Test script to verify JARVIS API endpoints are working
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /api/health...")
    try:
        response = requests.get(f"{API_URL}/api/health")
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"   Message: {data.get('message')}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print("\n🔍 Testing /api/status...")
    try:
        response = requests.get(f"{API_URL}/api/status")
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"   Components:")
        for name, status in data.get('components', {}).items():
            print(f"     - {name}: {status}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    print("\n🔍 Testing /api/chat...")
    try:
        message = "Hello JARVIS, how are you?"
        response = requests.post(
            f"{API_URL}/api/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        print(f"✅ Success: {data.get('success')}")
        print(f"   Message: {message}")
        print(f"   Response: {data.get('response', 'No response')}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_command():
    """Test command endpoint"""
    print("\n🔍 Testing /api/command...")
    try:
        command = "open calculator"
        response = requests.post(
            f"{API_URL}/api/command",
            json={"command": command},
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        print(f"✅ Success: {data.get('success')}")
        print(f"   Command: {command}")
        print(f"   Action: {data.get('action', 'unknown')}")
        print(f"   Result: {data.get('result', {})}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("JARVIS API CONNECTION TEST")
    print("=" * 60)
    print(f"Testing API at: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Health Check", test_health),
        ("System Status", test_status),
        ("Chat API", test_chat),
        ("Command API", test_command),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed! Backend is ready.")
    else:
        print("⚠️  Some tests failed. Check if Flask server is running.")
    
    return failed == 0

if __name__ == "__main__":
    exit(0 if main() else 1)
