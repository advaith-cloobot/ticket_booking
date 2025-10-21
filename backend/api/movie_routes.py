from flask import Blueprint, request, jsonify
from models import db, Movie, Showtime, Theater
from sqlalchemy import and_, or_

movie_bp = Blueprint('movies', __name__)

@movie_bp.route('/movies', methods=['GET'])
def get_movies():
    try:
        search_query = request.args.get('q', '')
        
        query = Movie.query
        
        if search_query:
            query = query.filter(
                or_(
                    Movie.title.ilike(f'%{search_query}%'),
                    Movie.genre.ilike(f'%{search_query}%'),
                    Movie.director.ilike(f'%{search_query}%')
                )
            )
        
        movies = query.all()
        
        movies_data = []
        for movie in movies:
            movies_data.append({
                'id': movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'director': movie.director,
                'duration_minutes': movie.duration_minutes,
                'release_date': movie.release_date.isoformat() if movie.release_date else None,
                'poster_url': movie.poster_url,
                'description': movie.description
            })
        
        return jsonify(movies_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_details(movie_id):
    try:
        movie = Movie.query.get(movie_id)
        
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
        
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'genre': movie.genre,
            'director': movie.director,
            'duration_minutes': movie.duration_minutes,
            'release_date': movie.release_date.isoformat() if movie.release_date else None,
            'poster_url': movie.poster_url,
            'description': movie.description
        }
        
        return jsonify(movie_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/movies/<int:movie_id>/showtimes', methods=['GET'])
def get_movie_showtimes(movie_id):
    try:
        movie = Movie.query.get(movie_id)
        
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
        
        showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
        
        showtimes_data = []
        for showtime in showtimes:
            showtimes_data.append({
                'id': showtime.id,
                'movie_id': showtime.movie_id,
                'theater_id': showtime.theater_id,
                'theater_name': showtime.theater.name,
                'theater_location': showtime.theater.location,
                'show_time': showtime.show_time.isoformat(),
                'ticket_price': float(showtime.ticket_price)
            })
        
        return jsonify(showtimes_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/showtimes/<int:showtime_id>', methods=['GET'])
def get_showtime_details(showtime_id):
    try:
        showtime = Showtime.query.get(showtime_id)
        
        if not showtime:
            return jsonify({'error': 'Showtime not found'}), 404
        
        showtime_data = {
            'id': showtime.id,
            'movie_id': showtime.movie_id,
            'movie_title': showtime.movie.title,
            'movie_poster': showtime.movie.poster_url,
            'theater_id': showtime.theater_id,
            'theater_name': showtime.theater.name,
            'theater_location': showtime.theater.location,
            'show_time': showtime.show_time.isoformat(),
            'ticket_price': float(showtime.ticket_price)
        }
        
        return jsonify(showtime_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movie_bp.route('/theaters', methods=['GET'])
def get_theaters():
    try:
        theaters = Theater.query.all()
        
        theaters_data = []
        for theater in theaters:
            theaters_data.append({
                'id': theater.id,
                'name': theater.name,
                'location': theater.location,
                'total_seats': theater.total_seats
            })
        
        return jsonify(theaters_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
