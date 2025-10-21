#!/usr/bin/env python3
"""
Complete test: Create booking and test PDF generation
"""

import requests
import json

def test_complete_booking_pdf():
    print("🎬 Complete Booking & PDF Test")
    print("=" * 40)
    
    base_url = "http://localhost:5000/api"
    
    # Test user
    test_user = {
        "name": "Complete Test User",
        "email": "complete@example.com",
        "password": "password123"
    }
    
    # Step 1: Create user
    print("\n1. Creating user...")
    try:
        response = requests.post(f"{base_url}/signup", json=test_user)
        print(f"Signup: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
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
    
    # Step 3: Get movies
    print("\n3. Getting movies...")
    try:
        response = requests.get(f"{base_url}/movies")
        if response.status_code == 200:
            movies = response.json()  # API returns array directly
            if movies and len(movies) > 0:
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
    
    # Step 4: Get showtimes
    print("\n4. Getting showtimes...")
    try:
        response = requests.get(f"{base_url}/movies/{movie_id}/showtimes")
        if response.status_code == 200:
            showtimes = response.json()  # API returns array directly
            if showtimes and len(showtimes) > 0:
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
    
    # Step 5: Create booking
    print("\n5. Creating booking...")
    try:
        booking_data = {
            "showtime_id": showtime_id,
            "seats": ["Z1", "Z2"]
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
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        return
    
    # Step 6: Process payment
    print("\n6. Processing payment...")
    try:
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
        print(f"❌ Error processing payment: {e}")
        return
    
    # Step 7: Test PDF download
    print(f"\n7. Testing PDF download for ticket: {ticket_id}")
    try:
        pdf_response = requests.get(f"{base_url}/ticket/{ticket_id}/download", headers=headers)
        
        print(f"PDF Status: {pdf_response.status_code}")
        print(f"Content-Type: {pdf_response.headers.get('Content-Type')}")
        print(f"Content-Length: {len(pdf_response.content)}")
        
        if pdf_response.status_code == 200:
            content_type = pdf_response.headers.get('Content-Type')
            if content_type == 'application/pdf':
                print("✅ PDF generated successfully!")
                
                # Save PDF
                filename = f"ticket_{ticket_id}.pdf"
                with open(filename, "wb") as f:
                    f.write(pdf_response.content)
                print(f"✅ PDF saved as: {filename}")
                print(f"PDF size: {len(pdf_response.content)} bytes")
            else:
                print(f"❌ Wrong content type: {content_type}")
                print(f"Response preview: {pdf_response.text[:200]}")
        else:
            print(f"❌ PDF download failed: {pdf_response.text}")
            
    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")
    
    print(f"\n🎉 Complete test finished!")

if __name__ == "__main__":
    test_complete_booking_pdf()
