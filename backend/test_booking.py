#!/usr/bin/env python3
"""
Test booking functionality
"""

import requests
import json

def test_booking():
    base_url = "http://localhost:5000/api"
    
    print("🧪 Testing Booking Functionality")
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
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test booking with valid showtime ID
    print("\n🎫 Testing booking initiation...")
    booking_data = {
        "showtime_id": 1,  # Use a valid showtime ID
        "seats": ["B1", "B2"]  # Use different seats
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{base_url}/book/initiate", json=booking_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Booking initiation successful")
            booking_info = response.json()
            print(f"Booking ID: {booking_info.get('booking_id')}")
            print(f"Ticket ID: {booking_info.get('ticket_id')}")
            print(f"Total Amount: {booking_info.get('total_amount')}")
        else:
            print(f"❌ Booking failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Booking error: {e}")

if __name__ == "__main__":
    test_booking()
