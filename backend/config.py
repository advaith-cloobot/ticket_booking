import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    # Use SQLite database - creates movie_ticket.db file in backend directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///movie_ticket.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration removed - no OTP functionality
    # Bookings are completed directly after payment confirmation
