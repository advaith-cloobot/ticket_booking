import React from 'react';
import { Link } from 'react-router-dom';

const MovieCard = ({ movie }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {movie.poster_url && (
        <img
          src={movie.poster_url}
          alt={movie.title}
          className="w-full h-64 object-cover"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x400?text=No+Image';
          }}
        />
      )}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          {movie.title}
        </h3>
        <p className="text-sm text-gray-600 mb-2">
          <span className="font-medium">Genre:</span> {movie.genre || 'N/A'}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <span className="font-medium">Director:</span> {movie.director || 'N/A'}
        </p>
        <p className="text-sm text-gray-600 mb-2">
          <span className="font-medium">Duration:</span> {movie.duration_minutes ? `${movie.duration_minutes} min` : 'N/A'}
        </p>
        {movie.description && (
          <p className="text-sm text-gray-700 mb-4 line-clamp-3">
            {movie.description}
          </p>
        )}
        <div className="flex justify-between items-center">
          <Link
            to={`/movie/${movie.id}`}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors duration-200 text-sm font-medium"
          >
            View Details
          </Link>
          {movie.release_date && (
            <span className="text-xs text-gray-500">
              {new Date(movie.release_date).getFullYear()}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
