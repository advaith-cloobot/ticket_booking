import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { moviesAPI } from '../api';
import MovieCard from '../components/MovieCard';
import SearchBar from '../components/SearchBar';

const HomePage = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchMovies();
  }, []);

  const fetchMovies = async (query = '') => {
    try {
      setLoading(true);
      const response = await moviesAPI.getMovies(query);
      setMovies(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch movies');
      console.error('Error fetching movies:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchMovies(searchQuery);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading movies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Movie Ticket Booking
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            Book your favorite movies and enjoy the show!
          </p>
          
          <SearchBar
            searchQuery={searchQuery}
            onSearchChange={handleSearchChange}
            onSearchSubmit={handleSearchSubmit}
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {movies.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No movies found</p>
            {searchQuery && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  fetchMovies();
                }}
                className="mt-4 text-indigo-600 hover:text-indigo-500"
              >
                Clear search
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {movies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
