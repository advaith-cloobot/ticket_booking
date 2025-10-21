#!/usr/bin/env python3
"""
Test JWT token format and validation
"""

import requests
import json
import jwt
from datetime import datetime

def test_token_format():
    base_url = "http://localhost:5000/api"
    
    print("🔍 Testing JWT Token Format")
    print("=" * 50)
    
    # Login to get a fresh token
    print("🔐 Logging in to get fresh token...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            user_data = data['user']
            
            print("✅ Login successful")
            print(f"User ID: {user_data['id']} (type: {type(user_data['id'])})")
            print(f"Token: {token[:50]}...")
            
            # Decode the token to see its contents
            try:
                # Decode without verification to see the payload
                decoded = jwt.decode(token, options={"verify_signature": False})
                print(f"\n🔍 Token payload:")
                print(f"Subject (sub): {decoded.get('sub')} (type: {type(decoded.get('sub'))})")
                print(f"Expiration: {decoded.get('exp')}")
                print(f"Full payload: {decoded}")
                
                # Check if subject is string
                if isinstance(decoded.get('sub'), str):
                    print("✅ Token subject is a string - GOOD")
                else:
                    print("❌ Token subject is not a string - BAD")
                    
            except Exception as e:
                print(f"❌ Error decoding token: {e}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test booking with the token
    print(f"\n🎫 Testing booking with token...")
    booking_data = {
        "showtime_id": 1,
        "seats": ["F1", "F2"]
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{base_url}/book/initiate", json=booking_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Booking successful with fresh token")
        else:
            print(f"❌ Booking failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Booking error: {e}")

if __name__ == "__main__":
    test_token_format()
