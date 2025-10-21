#!/usr/bin/env python3
"""
Test API response structure
"""

import requests
import json

def test_api_structure():
    print("🔍 Testing API Response Structure")
    print("=" * 40)
    
    base_url = "http://localhost:5000/api"
    
    # Test movies endpoint
    print("\n1. Testing /movies endpoint...")
    try:
        response = requests.get(f"{base_url}/movies")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response structure: {json.dumps(data, indent=2)[:500]}...")
            
            if 'movies' in data:
                movies = data['movies']
                print(f"Movies type: {type(movies)}")
                print(f"Movies length: {len(movies) if isinstance(movies, list) else 'Not a list'}")
                
                if movies and len(movies) > 0:
                    print(f"First movie: {movies[0]}")
            else:
                print("❌ 'movies' key not found")
        else:
            print(f"❌ API call failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_structure()
