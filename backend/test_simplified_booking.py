#!/usr/bin/env python3
"""
Test the simplified booking flow (no OTP)
"""

import requests
import json

def test_simplified_booking():
    print("🎬 Testing Simplified Booking Flow (No OTP)")
    print("=" * 50)
    
    base_url = "http://localhost:5000/api"
    
    # Test data
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    # Step 1: Sign up user
    print("\n1. Creating test user...")
    try:
        response = requests.post(f"{base_url}/signup", json=test_user)
        if response.status_code == 201:
            print("✅ User created successfully")
        elif response.status_code == 400 and "already exists" in response.text:
            print("✅ User already exists")
        else:
            print(f"❌ User creation failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating user: {e}")
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
    
    # Step 3: Get movies to find a showtime
    print("\n3. Getting movies...")
    try:
        response = requests.get(f"{base_url}/movies")
        if response.status_code == 200:
            movies = response.json()["movies"]
            if movies:
                movie_id = movies[0]["id"]
                print(f"✅ Found movie: {movies[0]['title']}")
            else:
                print("❌ No movies found")
                return
        else:
            print(f"❌ Failed to get movies: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error getting movies: {e}")
        return
    
    # Step 4: Get showtimes for the movie
    print("\n4. Getting showtimes...")
    try:
        response = requests.get(f"{base_url}/movies/{movie_id}/showtimes")
        if response.status_code == 200:
            showtimes = response.json()["showtimes"]
            if showtimes:
                showtime_id = showtimes[0]["id"]
                print(f"✅ Found showtime: {showtimes[0]['show_time']}")
            else:
                print("❌ No showtimes found")
                return
        else:
            print(f"❌ Failed to get showtimes: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error getting showtimes: {e}")
        return
    
    # Step 5: Initiate booking
    print("\n5. Initiating booking...")
    try:
        booking_data = {
            "showtime_id": showtime_id,
            "seats": ["A1", "A2"]
        }
        response = requests.post(f"{base_url}/book/initiate", json=booking_data, headers=headers)
        
        if response.status_code == 201:
            booking_info = response.json()
            booking_id = booking_info["booking_id"]
            print(f"✅ Booking initiated: {booking_info['ticket_id']}")
            print(f"   Total amount: ${booking_info['total_amount']}")
        else:
            print(f"❌ Booking initiation failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error initiating booking: {e}")
        return
    
    # Step 6: Process payment (complete booking)
    print("\n6. Processing payment...")
    try:
        payment_data = {
            "booking_id": booking_id,
            "payment_method": "card",
            "payment_reference": f"PAY_{booking_id}"
        }
        response = requests.post(f"{base_url}/book/payment", json=payment_data, headers=headers)
        
        if response.status_code == 200:
            payment_info = response.json()
            print(f"✅ Payment processed successfully!")
            print(f"   Booking ID: {payment_info['booking_id']}")
            print(f"   Ticket ID: {payment_info['ticket_id']}")
            print(f"   Status: {payment_info['status']}")
        else:
            print(f"❌ Payment processing failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error processing payment: {e}")
        return
    
    # Step 7: Get user's tickets
    print("\n7. Getting user tickets...")
    try:
        response = requests.get(f"{base_url}/my-tickets", headers=headers)
        
        if response.status_code == 200:
            tickets = response.json()["tickets"]
            print(f"✅ Found {len(tickets)} ticket(s)")
            for ticket in tickets:
                print(f"   - {ticket['movie_title']} at {ticket['theater_name']}")
                print(f"     Seats: {', '.join(ticket['seats'])}")
                print(f"     Status: {ticket['status']}")
        else:
            print(f"❌ Failed to get tickets: {response.text}")
    except Exception as e:
        print(f"❌ Error getting tickets: {e}")
    
    print(f"\n🎉 Simplified booking flow test completed!")
    print("✅ No OTP required - booking completed directly after payment")

if __name__ == "__main__":
    test_simplified_booking()
