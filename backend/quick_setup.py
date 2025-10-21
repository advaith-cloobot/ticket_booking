#!/usr/bin/env python3
"""
Quick setup script for Movie Ticket Booking Database
This script will help you set up the database for DataGrip viewing
"""

import os
import sys
from app import create_app
from models import db
from sample_data import create_sample_data

def setup_database():
    """Initialize the database and create sample data"""
    print("🎬 Movie Ticket Booking Database Setup")
    print("=" * 50)
    
    # Check database type
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///movie_ticket.db')
    
    if 'postgresql' in database_url:
        print("✅ PostgreSQL database detected")
        print(f"Database URL: {database_url}")
    else:
        print("✅ Using SQLite database")
        print(f"Database file: movie_ticket.db")
        print("📁 Database file will be created in the backend directory")
        print()
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if data already exists
            from models import Movie
            existing_movies = Movie.query.count()
            
            if existing_movies > 0:
                print(f"📋 Found {existing_movies} existing movies in database")
                print("Skipping sample data creation...")
            else:
                # Populate with sample data
                print("🎭 Populating with sample data...")
                create_sample_data()
                print("✅ Sample data created successfully!")
            
            print("\n🎉 Database setup completed!")
            print("\n📋 Database contains:")
            
            # Show table counts
            from models import User, Movie, Theater, Showtime, Booking, BookedSeat
            
            print(f"  👥 Users: {User.query.count()}")
            print(f"  🎬 Movies: {Movie.query.count()}")
            print(f"  🏢 Theaters: {Theater.query.count()}")
            print(f"  🎫 Showtimes: {Showtime.query.count()}")
            print(f"  📝 Bookings: {Booking.query.count()}")
            print(f"  💺 Booked Seats: {BookedSeat.query.count()}")
            
            print("\n🔗 DataGrip Connection Details:")
            if 'postgresql' in database_url:
                # Parse PostgreSQL URL
                import re
                match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', database_url)
                if match:
                    user, password, host, port, database = match.groups()
                    print(f"  Host: {host}")
                    print(f"  Port: {port}")
                    print(f"  Database: {database}")
                    print(f"  Username: {user}")
                    print(f"  Password: {password}")
            else:
                print("  📁 SQLite Database File: movie_ticket.db")
                print("  📍 Location: backend/movie_ticket.db")
                print("  🔗 DataGrip: File > New > Data Source > SQLite")
                print("  📂 Browse to: backend/movie_ticket.db")
                print("  💡 Alternative: Use SQLite Browser or DB Browser for SQLite")
            
            print("\n🚀 You can now run the Flask server with: python app.py")
            
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure PostgreSQL is running (if using PostgreSQL)")
            print("2. Check your DATABASE_URL environment variable")
            print("3. Ensure all dependencies are installed: pip install -r requirements.txt")
            sys.exit(1)

if __name__ == "__main__":
    setup_database()
