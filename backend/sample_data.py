from app import create_app
from models import db, User, Movie, Theater, Showtime
from datetime import datetime, timedelta
import random

def create_sample_data():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Clear existing data
        db.session.query(Showtime).delete()
        db.session.query(Movie).delete()
        db.session.query(Theater).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create sample movies
        movies = [
            Movie(
                title="The Dark Knight",
                genre="Action",
                director="Christopher Nolan",
                duration_minutes=152,
                release_date=datetime(2008, 7, 18).date(),
                poster_url="https://via.placeholder.com/300x400?text=The+Dark+Knight",
                description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
            ),
            Movie(
                title="Inception",
                genre="Sci-Fi",
                director="Christopher Nolan",
                duration_minutes=148,
                release_date=datetime(2010, 7, 16).date(),
                poster_url="https://via.placeholder.com/300x400?text=Inception",
                description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
            ),
            Movie(
                title="Interstellar",
                genre="Sci-Fi",
                director="Christopher Nolan",
                duration_minutes=169,
                release_date=datetime(2014, 11, 7).date(),
                poster_url="https://via.placeholder.com/300x400?text=Interstellar",
                description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
            ),
            Movie(
                title="The Shawshank Redemption",
                genre="Drama",
                director="Frank Darabont",
                duration_minutes=142,
                release_date=datetime(1994, 9, 23).date(),
                poster_url="https://via.placeholder.com/300x400?text=Shawshank",
                description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
            ),
            Movie(
                title="Pulp Fiction",
                genre="Crime",
                director="Quentin Tarantino",
                duration_minutes=154,
                release_date=datetime(1994, 10, 14).date(),
                poster_url="https://via.placeholder.com/300x400?text=Pulp+Fiction",
                description="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
            )
        ]
        
        for movie in movies:
            db.session.add(movie)
        
        # Create sample theaters
        theaters = [
            Theater(
                name="AMC Theater Downtown",
                location="123 Main St, Downtown",
                total_seats=200
            ),
            Theater(
                name="Regal Cinemas Mall",
                location="456 Mall Ave, Shopping District",
                total_seats=150
            ),
            Theater(
                name="Cinemark Multiplex",
                location="789 Theater Blvd, Entertainment Zone",
                total_seats=300
            )
        ]
        
        for theater in theaters:
            db.session.add(theater)
        
        db.session.commit()
        
        # Create sample showtimes
        showtimes = []
        base_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        for movie in movies:
            for theater in theaters:
                # Create 3 showtimes per day for 7 days
                for day in range(7):
                    for show_num in range(3):
                        show_time = base_time + timedelta(days=day, hours=show_num * 4)
                        showtime = Showtime(
                            movie_id=movie.id,
                            theater_id=theater.id,
                            show_time=show_time,
                            ticket_price=round(random.uniform(8.99, 15.99), 2)
                        )
                        showtimes.append(showtime)
        
        for showtime in showtimes:
            db.session.add(showtime)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        print(f"Created {len(movies)} movies")
        print(f"Created {len(theaters)} theaters")
        print(f"Created {len(showtimes)} showtimes")

if __name__ == "__main__":
    create_sample_data()
