#!/usr/bin/env python3
"""
Test script to verify the API endpoints are working
"""

import requests
import json

def test_api():
    base_url = "http://localhost:5000/api"
    
    print("🧪 Testing Movie Ticket Booking API")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://localhost:5000/")
        print("✅ Server is running")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server not running: {e}")
        print("Please start the server with: python app.py")
        return
    
    # Test 2: Test signup
    print("\n📝 Testing signup...")
    signup_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/signup", json=signup_data)
        if response.status_code == 201:
            print("✅ Signup successful")
            data = response.json()
            print(f"User ID: {data['user']['id']}")
            print(f"Email: {data['user']['email']}")
            print(f"Token: {data['access_token'][:20]}...")
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Signup error: {e}")
    
    # Test 3: Test login
    print("\n🔐 Testing login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful")
            data = response.json()
            print(f"User ID: {data['user']['id']}")
            print(f"Email: {data['user']['email']}")
            print(f"Token: {data['access_token'][:20]}...")
            
            # Test 4: Test protected route
            print("\n🔒 Testing protected route...")
            headers = {"Authorization": f"Bearer {data['access_token']}"}
            profile_response = requests.get(f"{base_url}/profile", headers=headers)
            
            if profile_response.status_code == 200:
                print("✅ Protected route accessible")
                print(f"Profile: {profile_response.json()}")
            else:
                print(f"❌ Protected route failed: {profile_response.status_code}")
                print(f"Error: {profile_response.text}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 5: Test movies endpoint
    print("\n🎬 Testing movies endpoint...")
    try:
        response = requests.get(f"{base_url}/movies")
        if response.status_code == 200:
            movies = response.json()
            print(f"✅ Movies endpoint working - {len(movies)} movies found")
            if movies:
                print(f"First movie: {movies[0]['title']}")
        else:
            print(f"❌ Movies endpoint failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Movies error: {e}")

if __name__ == "__main__":
    test_api()
