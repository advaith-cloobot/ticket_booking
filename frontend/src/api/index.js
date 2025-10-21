import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API calls
export const authAPI = {
  signup: (userData) => api.post('/signup', userData),
  login: (credentials) => api.post('/login', credentials),
  getProfile: () => api.get('/profile'),
};

// Movies API calls
export const moviesAPI = {
  getMovies: (searchQuery = '') => api.get(`/movies?q=${searchQuery}`),
  getMovieDetails: (movieId) => api.get(`/movies/${movieId}`),
  getMovieShowtimes: (movieId) => api.get(`/movies/${movieId}/showtimes`),
  getShowtimeDetails: (showtimeId) => api.get(`/showtimes/${showtimeId}`),
  getTheaters: () => api.get('/theaters'),
};

// Booking API calls
export const bookingAPI = {
  initiateBooking: (bookingData) => api.post('/book/initiate', bookingData),
  processPayment: (paymentData) => api.post('/book/payment', paymentData),
  getMyTickets: () => api.get('/my-tickets'),
  downloadTicket: (ticketId) => api.get(`/ticket/${ticketId}/download`, { responseType: 'blob' }),
};

export default api;
