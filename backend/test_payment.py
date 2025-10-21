#!/usr/bin/env python3
"""
Test payment processing and OTP generation
"""

import requests
import json

def test_payment_flow():
    base_url = "http://localhost:5000/api"
    
    print("💳 Testing Payment Flow")
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
    
    # Create a booking first
    print("\n🎫 Creating booking...")
    booking_data = {
        "showtime_id": 1,
        "seats": ["G1", "G2"]
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{base_url}/book/initiate", json=booking_data, headers=headers)
        if response.status_code == 201:
            booking_info = response.json()
            booking_id = booking_info['booking_id']
            print(f"✅ Booking created - ID: {booking_id}")
        else:
            print(f"❌ Booking failed: {response.status_code}")
            print(f"Error: {response.text}")
            return
    except Exception as e:
        print(f"❌ Booking error: {e}")
        return
    
    # Test payment processing
    print(f"\n💳 Testing payment processing...")
    payment_data = {
        "booking_id": booking_id
    }
    
    try:
        response = requests.post(f"{base_url}/book/payment", json=payment_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            payment_info = response.json()
            print("✅ Payment processing successful")
            
            # Check if OTP is in response
            if 'otp' in payment_info:
                otp = payment_info['otp']
                print(f"🔑 OTP for testing: {otp}")
                
                # Test OTP verification
                print(f"\n🔐 Testing OTP verification...")
                otp_data = {
                    "booking_id": booking_id,
                    "otp": otp
                }
                
                verify_response = requests.post(f"{base_url}/book/verify", json=otp_data, headers=headers)
                print(f"Verify Status: {verify_response.status_code}")
                print(f"Verify Response: {verify_response.text}")
                
                if verify_response.status_code == 200:
                    print("✅ OTP verification successful!")
                    verify_info = verify_response.json()
                    print(f"Ticket ID: {verify_info.get('ticket_id')}")
                else:
                    print(f"❌ OTP verification failed: {verify_response.text}")
            else:
                print("ℹ️  OTP not in response (email configured)")
        else:
            print(f"❌ Payment processing failed: {response.text}")
    except Exception as e:
        print(f"❌ Payment error: {e}")

if __name__ == "__main__":
    test_payment_flow()
