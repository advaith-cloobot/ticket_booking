import React, { useState, useEffect } from 'react';

const SeatPicker = ({ showtimeId, onSeatsChange, bookedSeats = [] }) => {
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [seats, setSeats] = useState([]);

  useEffect(() => {
    // Generate seat layout (5 rows, 10 seats per row)
    const seatLayout = [];
    const rows = ['A', 'B', 'C', 'D', 'E'];
    
    rows.forEach(row => {
      for (let i = 1; i <= 10; i++) {
        seatLayout.push({
          id: `${row}${i}`,
          row: row,
          number: i,
          isBooked: bookedSeats.includes(`${row}${i}`),
          isSelected: false
        });
      }
    });
    
    setSeats(seatLayout);
  }, [bookedSeats]);

  const handleSeatClick = (seatId) => {
    const seat = seats.find(s => s.id === seatId);
    
    if (seat.isBooked) return;
    
    const updatedSeats = seats.map(s => {
      if (s.id === seatId) {
        return { ...s, isSelected: !s.isSelected };
      }
      return s;
    });
    
    setSeats(updatedSeats);
    
    const newSelectedSeats = updatedSeats
      .filter(s => s.isSelected)
      .map(s => s.id);
    
    setSelectedSeats(newSelectedSeats);
    onSeatsChange(newSelectedSeats);
  };

  const getSeatColor = (seat) => {
    if (seat.isBooked) return 'bg-red-500 cursor-not-allowed';
    if (seat.isSelected) return 'bg-indigo-500 hover:bg-indigo-600';
    return 'bg-gray-300 hover:bg-gray-400';
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Your Seats</h3>
        <div className="flex justify-center mb-4">
          <div className="bg-gray-200 p-4 rounded-lg">
            <div className="text-center text-sm font-medium text-gray-600 mb-2">Screen</div>
            <div className="w-full h-2 bg-gray-400 rounded"></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-10 gap-2 mb-6">
        {seats.map((seat) => (
          <button
            key={seat.id}
            onClick={() => handleSeatClick(seat.id)}
            disabled={seat.isBooked}
            className={`
              w-8 h-8 rounded text-xs font-medium text-white transition-colors duration-200
              ${getSeatColor(seat)}
              ${seat.isBooked ? 'cursor-not-allowed' : 'cursor-pointer'}
            `}
          >
            {seat.number}
          </button>
        ))}
      </div>

      <div className="flex justify-center space-x-6 text-sm">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-gray-300 rounded mr-2"></div>
          <span>Available</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-indigo-500 rounded mr-2"></div>
          <span>Selected</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-red-500 rounded mr-2"></div>
          <span>Booked</span>
        </div>
      </div>

      {selectedSeats.length > 0 && (
        <div className="mt-4 p-4 bg-indigo-50 rounded-lg">
          <p className="text-sm text-indigo-800">
            Selected seats: {selectedSeats.join(', ')}
          </p>
        </div>
      )}
    </div>
  );
};

export default SeatPicker;
