# Database Setup for Movie Ticket Booking System

## PostgreSQL Database Setup

### Option 1: Using PostgreSQL with Docker (Recommended)

1. **Install Docker Desktop** (if not already installed)
2. **Run PostgreSQL container:**
   ```bash
   docker run --name movie-ticket-postgres \
     -e POSTGRES_DB=movie_ticket_db \
     -e POSTGRES_USER=movie_user \
     -e POSTGRES_PASSWORD=movie_password \
     -p 5432:5432 \
     -d postgres:13
   ```

3. **Database Connection Details:**
   - Host: localhost
   - Port: 5432
   - Database: movie_ticket_db
   - Username: movie_user
   - Password: movie_password

### Option 2: Install PostgreSQL Locally

1. **Download PostgreSQL** from https://www.postgresql.org/download/
2. **Install with default settings**
3. **Create database:**
   ```sql
   CREATE DATABASE movie_ticket_db;
   CREATE USER movie_user WITH PASSWORD 'movie_password';
   GRANT ALL PRIVILEGES ON DATABASE movie_ticket_db TO movie_user;
   ```

## Environment Configuration

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://movie_user:movie_password@localhost:5432/movie_ticket_db
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Initialize Database

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database:**
   ```bash
   python setup.py
   ```

## DataGrip Connection Setup

### Step 1: Open DataGrip
1. Launch DataGrip
2. Click "New Data Source" or "+" button

### Step 2: Configure PostgreSQL Connection
1. **Select PostgreSQL** from the database list
2. **Connection Details:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `movie_ticket_db`
   - User: `movie_user`
   - Password: `movie_password`

### Step 3: Test Connection
1. Click "Test Connection" to verify
2. If successful, click "OK" to save the connection

### Step 4: View Database Schema
Once connected, you'll see the following tables:
- `users` - User accounts
- `movies` - Movie information
- `theaters` - Theater details
- `showtimes` - Movie showtimes
- `bookings` - Booking records
- `booked_seats` - Seat reservations

## Sample Data

The database will be populated with sample data including:
- 5 sample movies (The Dark Knight, Inception, etc.)
- 3 sample theaters
- Multiple showtimes for each movie
- Sample user accounts (if created through the app)

## Troubleshooting

### Common Issues:
1. **Connection Refused**: Make sure PostgreSQL is running
2. **Authentication Failed**: Check username/password
3. **Database Not Found**: Run the setup script to create tables
4. **Permission Denied**: Ensure user has proper privileges

### Useful SQL Queries:
```sql
-- View all tables
\dt

-- View all users
SELECT * FROM users;

-- View all movies
SELECT * FROM movies;

-- View all bookings
SELECT * FROM bookings;

-- View bookings with user and movie details
SELECT 
    b.ticket_id,
    u.email,
    m.title,
    t.name as theater_name,
    b.total_amount,
    b.booking_status
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN showtimes s ON b.showtime_id = s.id
JOIN movies m ON s.movie_id = m.id
JOIN theaters t ON s.theater_id = t.id;
```
