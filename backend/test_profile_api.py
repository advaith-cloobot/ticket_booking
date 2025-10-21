#!/usr/bin/env python3
"""
Test the profile API to verify response structure
"""

import requests
import json

def test_profile_api():
    print("🧪 Testing Profile API Response Structure")
    print("=" * 50)
    
    base_url = "http://localhost:5000/api"
    
    # Test data
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    # Step 1: Create user
    print("\n1. Creating test user...")
    try:
        response = requests.post(f"{base_url}/signup", json=test_user)
        if response.status_code in [201, 400]:
            print("✅ User ready")
        else:
            print(f"❌ User creation failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Login
    print("\n2. Logging in...")
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{base_url}/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 3: Test my-tickets endpoint
    print("\n3. Testing /my-tickets endpoint...")
    try:
        response = requests.get(f"{base_url}/my-tickets", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received")
            print(f"Response structure: {json.dumps(data, indent=2)}")
            
            if 'tickets' in data:
                print(f"✅ 'tickets' key found")
                print(f"Tickets type: {type(data['tickets'])}")
                print(f"Tickets length: {len(data['tickets']) if isinstance(data['tickets'], list) else 'Not a list'}")
                
                if data['tickets']:
                    print(f"First ticket structure: {json.dumps(data['tickets'][0], indent=2)}")
                else:
                    print("No tickets found (empty array)")
            else:
                print("❌ 'tickets' key not found in response")
        else:
            print(f"❌ API call failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_profile_api()
