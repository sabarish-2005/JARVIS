#!/usr/bin/env python
"""
==================== JARVIS API TEST SCRIPT ====================
Test all API endpoints to ensure everything is working correctly
"""

import requests
import json
from typing import Dict, Any
import time

# Configuration
API_BASE = "http://localhost:5000/api"
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{COLORS['BOLD']}{COLORS['BLUE']}{'='*60}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['BLUE']}{text:^60}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['BLUE']}{'='*60}{COLORS['RESET']}\n")

def print_test(name: str, result: bool, message: str = ""):
    """Print test result"""
    status = f"{COLORS['GREEN']}✓ PASS{COLORS['RESET']}" if result else f"{COLORS['RED']}✗ FAIL{COLORS['RESET']}"
    print(f"  {status} - {name}")
    if message:
        print(f"    {COLORS['YELLOW']}{message}{COLORS['RESET']}")

def test_endpoint(method: str, endpoint: str, data: Dict = None, description: str = "") -> Dict[str, Any]:
    """Test an API endpoint"""
    try:
        url = f"{API_BASE}{endpoint}"
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            return {'success': False, 'error': f'Unknown method: {method}'}

        return {
            'success': response.status_code in [200, 201],
            'status_code': response.status_code,
            'data': response.json() if response.text else {},
            'description': description
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Connection failed. Is the API server running?',
            'description': description
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'description': description
        }

def main():
    """Run all API tests"""
    print_header("JARVIS API TEST SUITE")
    
    tests_passed = 0
    tests_failed = 0

    # Test 1: Health Check
    print_header("1. Health & Status Tests")
    result = test_endpoint("GET", "/health", description="Health Check")
    print_test("API Health", result['success'], result.get('error', 'API is running'))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    result = test_endpoint("GET", "/status", description="System Status")
    print_test("System Status", result['success'], result.get('error', 'All components ready'))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    # Test 2: Chat
    print_header("2. Chat Tests")
    result = test_endpoint("POST", "/chat", {"message": "Hello JARVIS"}, "Chat Request")
    print_test("Chat with AI", result['success'], result.get('error', 'Response received'))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    # Test 3: Commands
    print_header("3. Command Tests")
    result = test_endpoint("POST", "/parse", {"command": "play music on youtube"}, "Parse Command")
    print_test("Parse Command", result['success'], result.get('error', 'Intent parsed'))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    result = test_endpoint("POST", "/command", {"command": "what time is it"}, "Execute Command")
    print_test("Execute Command", result['success'], result.get('error', 'Command executed'))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    # Test 4: Actions
    print_header("4. Supported Actions")
    result = test_endpoint("GET", "/actions", description="Get Actions")
    print_test("Get Supported Actions", result['success'], result.get('error', ''))
    if result['success']:
        tests_passed += 1
        if 'data' in result and 'actions' in result['data']:
            num_actions = len(result['data']['actions'])
            print(f"    Found {num_actions} supported actions")
    else:
        tests_failed += 1

    # Test 5: System
    print_header("5. System Control Tests")
    result = test_endpoint("GET", "/time", description="Get Time")
    print_test("Get Current Time", result['success'], result.get('error', ''))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    result = test_endpoint("GET", "/date", description="Get Date")
    print_test("Get Current Date", result['success'], result.get('error', ''))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    result = test_endpoint("POST", "/system/volume", {"action": "up"}, "Volume Control")
    print_test("Control Volume", result['success'], result.get('error', ''))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    # Test 6: Browser
    print_header("6. Browser Control Tests")
    result = test_endpoint("POST", "/browser/google", {"query": "python tutorial"}, "Google Search")
    print_test("Google Search", result['success'], result.get('error', ''))
    if result['success']: tests_passed += 1
    else: tests_failed += 1

    # Test 7: Error Handling
    print_header("7. Error Handling Tests")
    result = test_endpoint("POST", "/chat", {"message": ""}, "Empty Message")
    print_test("Handle Empty Input", not result['success'], 'Should return error for empty input')
    if not result['success']: tests_passed += 1
    else: tests_failed += 1

    result = test_endpoint("GET", "/nonexistent", description="Non-existent Endpoint")
    print_test("Handle 404 Error", result['status_code'] == 404, 'Should return 404')
    if result['status_code'] == 404: tests_passed += 1
    else: tests_failed += 1

    # Summary
    print_header("TEST SUMMARY")
    total = tests_passed + tests_failed
    percentage = (tests_passed / total * 100) if total > 0 else 0
    
    print(f"{COLORS['BOLD']}{COLORS['GREEN']}Passed: {tests_passed}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}{COLORS['RED']}Failed: {tests_failed}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}Total:  {total}{COLORS['RESET']}")
    print(f"{COLORS['BOLD']}Success Rate: {percentage:.1f}%{COLORS['RESET']}\n")

    if tests_failed == 0:
        print(f"{COLORS['GREEN']}{COLORS['BOLD']}✓ All tests passed! API is ready to use.{COLORS['RESET']}\n")
    else:
        print(f"{COLORS['RED']}{COLORS['BOLD']}✗ Some tests failed. Check the API server.{COLORS['RESET']}\n")

    print("="*60)

if __name__ == "__main__":
    print(f"{COLORS['YELLOW']}Connecting to JARVIS API at {API_BASE}...{COLORS['RESET']}")
    time.sleep(1)
    main()
