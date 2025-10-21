# SQLite Database Setup for Movie Ticket Booking

## Quick Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python quick_setup.py
```

This will create:
- `movie_ticket.db` file in the backend directory
- All necessary tables
- Sample data (movies, theaters, showtimes)

## Viewing the Database

### Option 1: DataGrip (JetBrains)
1. Open DataGrip
2. Click **"New Data Source"** or **"+"**
3. Select **SQLite**
4. Browse to: `backend/movie_ticket.db`
5. Click **"Test Connection"** then **"OK"**

### Option 2: DB Browser for SQLite (Free)
1. Download from: https://sqlitebrowser.org/
2. Open DB Browser for SQLite
3. Click **"Open Database"**
4. Navigate to: `backend/movie_ticket.db`
5. Click **"Open"**

### Option 3: SQLite Command Line
```bash
# Navigate to backend directory
cd backend

# Open SQLite database
sqlite3 movie_ticket.db

# View tables
.tables

# View table structure
.schema users

# Run queries
SELECT * FROM movies;
SELECT * FROM users;
SELECT * FROM bookings;

# Exit
.quit
```

## Database Schema

The SQLite database contains these tables:

| Table | Description |
|-------|-------------|
| `users` | User accounts and authentication |
| `movies` | Movie information (title, genre, director, etc.) |
| `theaters` | Theater details (name, location, capacity) |
| `showtimes` | Movie showtimes (movie_id, theater_id, show_time, price) |
| `bookings` | Booking records (ticket_id, user_id, showtime_id, amount, status) |
| `booked_seats` | Seat reservations (booking_id, seat_id) |

## Sample Data

The database will be populated with:

### Movies (5 sample movies)
- The Dark Knight
- Inception
- Interstellar
- The Shawshank Redemption
- Pulp Fiction

### Theaters (3 sample theaters)
- AMC Theater Downtown
- Regal Cinemas Mall
- Cinemark Multiplex

### Showtimes
- Multiple showtimes for each movie
- Different theaters and times
- Various ticket prices

## Useful SQL Queries

```sql
-- View all movies
SELECT * FROM movies;

-- View all theaters
SELECT * FROM theaters;

-- View all showtimes with movie and theater details
SELECT 
    m.title,
    t.name as theater_name,
    s.show_time,
    s.ticket_price
FROM showtimes s
JOIN movies m ON s.movie_id = m.id
JOIN theaters t ON s.theater_id = t.id
ORDER BY m.title, s.show_time;

-- View all bookings with user and movie details
SELECT 
    b.ticket_id,
    u.email,
    m.title,
    t.name as theater_name,
    b.total_amount,
    b.booking_status,
    b.created_at
FROM bookings b
JOIN users u ON b.user_id = u.id
JOIN showtimes s ON b.showtime_id = s.id
JOIN movies m ON s.movie_id = m.id
JOIN theaters t ON s.theater_id = t.id
ORDER BY b.created_at DESC;

-- View booked seats for a specific showtime
SELECT 
    bs.seat_id,
    b.ticket_id,
    u.email,
    b.booking_status
FROM booked_seats bs
JOIN bookings b ON bs.booking_id = b.id
JOIN users u ON b.user_id = u.id
WHERE b.showtime_id = 1;
```

## File Location

The SQLite database file will be created at:
```
backend/movie_ticket.db
```

You can copy this file to view it in any SQLite browser or share it with others.
