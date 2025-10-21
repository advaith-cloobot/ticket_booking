#!/usr/bin/env python3
"""
Simple test for PDF generation
"""

import requests
import json

def test_simple_pdf():
    print("🎫 Simple PDF Test")
    print("=" * 30)
    
    base_url = "http://localhost:5000/api"
    
    # Test with existing user or create new one
    test_user = {
        "name": "PDF Test User",
        "email": "pdftest@example.com",
        "password": "password123"
    }
    
    # Step 1: Sign up
    print("\n1. Creating user...")
    try:
        response = requests.post(f"{base_url}/signup", json=test_user)
        print(f"Signup response: {response.status_code}")
        if response.status_code not in [201, 400]:
            print(f"Response: {response.text}")
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
    
    # Step 3: Get tickets
    print("\n3. Getting user tickets...")
    try:
        response = requests.get(f"{base_url}/my-tickets", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            tickets = data.get('tickets', [])
            print(f"✅ Found {len(tickets)} ticket(s)")
            
            if tickets:
                ticket_id = tickets[0]['ticket_id']
                print(f"Testing PDF download for ticket: {ticket_id}")
                
                # Step 4: Download PDF
                print("\n4. Downloading PDF...")
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
                    else:
                        print(f"❌ Wrong content type: {content_type}")
                        print(f"Response: {pdf_response.text[:200]}")
                else:
                    print(f"❌ PDF download failed: {pdf_response.text}")
            else:
                print("❌ No tickets found - create a booking first")
        else:
            print(f"❌ Failed to get tickets: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple_pdf()
