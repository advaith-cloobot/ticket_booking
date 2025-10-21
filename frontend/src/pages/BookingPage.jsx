import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { moviesAPI, bookingAPI } from '../api';
import SeatPicker from '../components/SeatPicker';

const BookingPage = () => {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [showtime, setShowtime] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [bookedSeats, setBookedSeats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [booking, setBooking] = useState(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchShowtimeDetails();
  }, [showtimeId, user, navigate]);

  const fetchShowtimeDetails = async () => {
    try {
      const response = await moviesAPI.getShowtimeDetails(parseInt(showtimeId));
      const showtimeData = response.data;
      
      // Transform the API response to match the expected format
      const showtime = {
        id: showtimeData.id,
        movie: { 
          title: showtimeData.movie_title, 
          poster_url: showtimeData.movie_poster 
        },
        theater: { 
          name: showtimeData.theater_name, 
          location: showtimeData.theater_location 
        },
        show_time: showtimeData.show_time,
        ticket_price: showtimeData.ticket_price
      };
      
      setShowtime(showtime);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch showtime details');
      console.error('Error fetching showtime details:', err);
      setLoading(false);
    }
  };

  const handleSeatsChange = (seats) => {
    setSelectedSeats(seats);
  };

  const handleProceedToPayment = async () => {
    if (selectedSeats.length === 0) {
      setError('Please select at least one seat');
      return;
    }

    try {
      const response = await bookingAPI.initiateBooking({
        showtime_id: parseInt(showtimeId),
        seats: selectedSeats
      });
      
      setBooking(response.data);
      navigate('/payment', { 
        state: { 
          booking: response.data,
          showtime: showtime,
          selectedSeats: selectedSeats
        }
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to initiate booking');
      console.error('Error initiating booking:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading booking details...</p>
        </div>
      </div>
    );
  }

  if (error || !showtime) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg">{error || 'Showtime not found'}</p>
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

  const totalPrice = selectedSeats.length * showtime.ticket_price;

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

        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Book Your Tickets</h1>
            
            <div className="bg-gray-50 rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">{showtime.movie.title}</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Theater</p>
                  <p className="font-medium">{showtime.theater.name}</p>
                  <p className="text-sm text-gray-600">{showtime.theater.location}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Show Time</p>
                  <p className="font-medium">
                    {new Date(showtime.show_time).toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Price per Seat</p>
                  <p className="font-medium">${showtime.ticket_price}</p>
                </div>
              </div>
            </div>
          </div>

          <SeatPicker
            showtimeId={showtimeId}
            onSeatsChange={handleSeatsChange}
            bookedSeats={bookedSeats}
          />

          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {selectedSeats.length > 0 && (
            <div className="mt-8 bg-indigo-50 rounded-lg p-6">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm text-gray-600">Selected Seats</p>
                  <p className="font-medium">{selectedSeats.join(', ')}</p>
                  <p className="text-sm text-gray-600">
                    {selectedSeats.length} seat{selectedSeats.length > 1 ? 's' : ''} × ${showtime.ticket_price}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-indigo-600">
                    ${totalPrice.toFixed(2)}
                  </p>
                  <button
                    onClick={handleProceedToPayment}
                    className="mt-4 bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition-colors duration-200 font-medium"
                  >
                    Proceed to Payment
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BookingPage;
