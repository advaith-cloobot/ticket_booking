# Movie Ticket Booking System

A full-stack web application for booking movie tickets built with React frontend and Flask backend.

## Features

- User authentication (signup/login)
- Browse movies with search functionality
- View movie details and showtimes
- Interactive seat selection
- Payment processing with OTP verification
- Ticket management and PDF download
- Responsive design with modern UI

## Tech Stack

### Backend
- Python Flask
- SQLAlchemy (ORM)
- PostgreSQL database
- JWT authentication
- Flask-Mail for email notifications
- ReportLab for PDF generation

### Frontend
- React.js
- React Router for navigation
- Axios for API calls
- Tailwind CSS for styling
- Context API for state management

## Project Structure

```
movie-ticket-app/
├── backend/
│   ├── api/
│   │   ├── auth_routes.py      # Authentication endpoints
│   │   ├── movie_routes.py     # Movie-related endpoints
│   │   └── booking_routes.py   # Booking and payment endpoints
│   ├── models.py               # Database models
│   ├── app.py                  # Flask application
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   └── sample_data.py          # Sample data script
└── frontend/
    ├── src/
    │   ├── components/         # Reusable components
    │   ├── pages/             # Page components
    │   ├── context/           # React Context
    │   └── api/               # API integration
    └── package.json           # Node.js dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL database

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/movie_ticket_db
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

6. Create the database and run migrations:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. Populate with sample data:
   ```bash
   python sample_data.py
   ```

8. Run the Flask server:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   Create a `.env` file in the frontend directory with:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```

4. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `GET /api/profile` - Get user profile (protected)

### Movies
- `GET /api/movies` - Get all movies (with optional search)
- `GET /api/movies/<id>` - Get movie details
- `GET /api/movies/<id>/showtimes` - Get movie showtimes
- `GET /api/theaters` - Get all theaters

### Booking
- `POST /api/book/initiate` - Initiate booking (protected)
- `POST /api/book/payment` - Process payment (protected)
- `POST /api/book/verify` - Verify OTP (protected)
- `GET /api/my-tickets` - Get user tickets (protected)
- `GET /api/ticket/<ticket_id>/download` - Download ticket PDF (protected)

## Database Schema

The application uses the following main tables:
- `users` - User accounts
- `movies` - Movie information
- `theaters` - Theater details
- `showtimes` - Movie showtimes
- `bookings` - Booking records
- `booked_seats` - Seat reservations

## Features Overview

### User Authentication
- Secure user registration and login
- JWT-based authentication
- Password hashing with bcrypt

### Movie Management
- Browse movies with search functionality
- View detailed movie information
- Check available showtimes

### Booking System
- Interactive seat selection
- Real-time seat availability
- Multiple payment methods
- OTP verification for security

### Ticket Management
- View booking history
- Download tickets as PDF
- Ticket validation

## Development Notes

- The application uses CORS for cross-origin requests
- Email functionality requires proper SMTP configuration
- PDF generation uses ReportLab library
- Frontend uses Tailwind CSS for styling
- State management handled with React Context

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.