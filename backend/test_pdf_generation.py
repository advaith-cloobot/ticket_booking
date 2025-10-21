#!/usr/bin/env python3
"""
Test PDF generation for tickets
"""

import requests
import json

def test_pdf_generation():
    print("🎫 Testing PDF Ticket Generation")
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
    
    # Step 3: Get movies and create a booking
    print("\n3. Creating a test booking...")
    try:
        # Get movies
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
        
        # Get showtimes
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
        
        # Create booking
        booking_data = {
            "showtime_id": showtime_id,
            "seats": ["A1", "A2"]
        }
        response = requests.post(f"{base_url}/book/initiate", json=booking_data, headers=headers)
        
        if response.status_code == 201:
            booking_info = response.json()
            booking_id = booking_info["booking_id"]
            ticket_id = booking_info["ticket_id"]
            print(f"✅ Booking created: {ticket_id}")
        else:
            print(f"❌ Booking creation failed: {response.text}")
            return
        
        # Process payment
        payment_data = {
            "booking_id": booking_id,
            "payment_method": "card",
            "payment_reference": f"PAY_{booking_id}"
        }
        response = requests.post(f"{base_url}/book/payment", json=payment_data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Payment processed")
        else:
            print(f"❌ Payment failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        return
    
    # Step 4: Test PDF download
    print(f"\n4. Testing PDF download for ticket: {ticket_id}")
    try:
        response = requests.get(f"{base_url}/ticket/{ticket_id}/download", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Length: {len(response.content)}")
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/pdf':
                print("✅ PDF generated successfully!")
                print(f"PDF size: {len(response.content)} bytes")
                
                # Save PDF to file for testing
                with open(f"test_ticket_{ticket_id}.pdf", "wb") as f:
                    f.write(response.content)
                print(f"✅ PDF saved as: test_ticket_{ticket_id}.pdf")
                
            else:
                print(f"❌ Wrong content type: {content_type}")
                print(f"Response content: {response.text[:200]}...")
        else:
            print(f"❌ PDF download failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")
    
    print(f"\n🎉 PDF generation test completed!")

if __name__ == "__main__":
    test_pdf_generation()
