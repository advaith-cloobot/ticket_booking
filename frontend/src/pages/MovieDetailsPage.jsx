import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { moviesAPI } from '../api';

const MovieDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [showtimes, setShowtimes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMovieDetails();
    fetchShowtimes();
  }, [id]);

  const fetchMovieDetails = async () => {
    try {
      const response = await moviesAPI.getMovieDetails(id);
      setMovie(response.data);
    } catch (err) {
      setError('Failed to fetch movie details');
      console.error('Error fetching movie details:', err);
    }
  };

  const fetchShowtimes = async () => {
    try {
      const response = await moviesAPI.getMovieShowtimes(id);
      setShowtimes(response.data);
    } catch (err) {
      setError('Failed to fetch showtimes');
      console.error('Error fetching showtimes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleBookNow = (showtimeId) => {
    navigate(`/book/${showtimeId}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading movie details...</p>
        </div>
      </div>
    );
  }

  if (error || !movie) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg">{error || 'Movie not found'}</p>
          <button
            onClick={() => navigate('/')}
            className="mt-4 text-indigo-600 hover:text-indigo-500"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button
          onClick={() => navigate('/')}
          className="mb-6 text-indigo-600 hover:text-indigo-500 flex items-center"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Movies
        </button>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="md:flex">
            <div className="md:w-1/3">
              {movie.poster_url ? (
                <img
                  src={movie.poster_url}
                  alt={movie.title}
                  className="w-full h-96 md:h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/400x600?text=No+Image';
                  }}
                />
              ) : (
                <div className="w-full h-96 md:h-full bg-gray-200 flex items-center justify-center">
                  <span className="text-gray-500">No Image Available</span>
                </div>
              )}
            </div>
            <div className="md:w-2/3 p-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{movie.title}</h1>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-600">Genre</p>
                  <p className="font-medium">{movie.genre || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Director</p>
                  <p className="font-medium">{movie.director || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Duration</p>
                  <p className="font-medium">
                    {movie.duration_minutes ? `${movie.duration_minutes} minutes` : 'N/A'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Release Date</p>
                  <p className="font-medium">
                    {movie.release_date ? new Date(movie.release_date).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
              </div>

              {movie.description && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700">{movie.description}</p>
                </div>
              )}

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Showtimes</h3>
                {showtimes.length === 0 ? (
                  <p className="text-gray-500">No showtimes available</p>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {showtimes.map((showtime) => (
                      <div key={showtime.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="mb-2">
                          <p className="font-medium text-gray-900">{showtime.theater_name}</p>
                          <p className="text-sm text-gray-600">{showtime.theater_location}</p>
                        </div>
                        <div className="mb-3">
                          <p className="text-sm text-gray-600">Show Time</p>
                          <p className="font-medium">
                            {new Date(showtime.show_time).toLocaleString()}
                          </p>
                        </div>
                        <div className="flex justify-between items-center">
                          <p className="text-lg font-semibold text-indigo-600">
                            ${showtime.ticket_price}
                          </p>
                          <button
                            onClick={() => handleBookNow(showtime.id)}
                            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors duration-200 text-sm font-medium"
                          >
                            Book Now
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetailsPage;
