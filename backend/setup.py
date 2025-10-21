#!/usr/bin/env python3
"""
Setup script for the Movie Ticket Booking Backend
Run this script to initialize the database and populate sample data
"""

import os
import sys
from app import create_app
from models import db
from sample_data import create_sample_data

def setup_database():
    """Initialize the database and create sample data"""
    print("Setting up Movie Ticket Booking Database...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Populate with sample data
            print("Populating with sample data...")
            create_sample_data()
            print("✅ Sample data created successfully!")
            
            print("\n🎉 Setup completed successfully!")
            print("You can now run the Flask server with: python app.py")
            print("The API will be available at: http://localhost:5000")
            
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup_database()
