#!/usr/bin/env python3
"""
Test booking with string showtime ID to simulate frontend behavior
"""

import requests
import json

def test_frontend_booking():
    base_url = "http://localhost:5000/api"
    
    print("🧪 Testing Frontend-like Booking")
    print("=" * 50)
    
    # First, login to get a token
    print("🔐 Logging in...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test booking with string showtime ID (like frontend sends)
    print("\n🎫 Testing booking with string showtime ID...")
    booking_data = {
        "showtime_id": "1",  # String like frontend sends
        "seats": ["D1", "D2"]
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{base_url}/book/initiate", json=booking_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Booking with string ID successful")
        else:
            print(f"❌ Booking failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Booking error: {e}")

if __name__ == "__main__":
    test_frontend_booking()
