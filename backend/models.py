from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100))
    director = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    poster_url = db.Column(db.Text)
    description = db.Column(db.Text)
    
    # Relationships
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)

class Theater(db.Model):
    __tablename__ = 'theaters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.Text, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    
    # Relationships
    showtimes = db.relationship('Showtime', backref='theater', lazy=True)

class Showtime(db.Model):
    __tablename__ = 'showtimes'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theaters.id'), nullable=False)
    show_time = db.Column(db.DateTime, nullable=False)
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='showtime', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtimes.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    booking_status = db.Column(db.String(20), default='pending')
    otp = db.Column(db.String(6))
    otp_expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    booked_seats = db.relationship('BookedSeat', backref='booking', lazy=True, cascade='all, delete-orphan')

class BookedSeat(db.Model):
    __tablename__ = 'booked_seats'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    seat_id = db.Column(db.String(4), nullable=False)  # e.g., 'A1', 'F12'
