import React from 'react';
import { bookingAPI } from '../api';

const Ticket = ({ ticket }) => {
  const handleDownload = async () => {
    try {
      const response = await bookingAPI.downloadTicket(ticket.ticket_id);
      
      // Check if response is PDF
      const contentType = response.headers['content-type'];
      if (contentType === 'application/pdf') {
        // Create blob and download
        const blob = new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `ticket_${ticket.ticket_id}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } else {
        console.error('Invalid content type:', contentType);
        alert('Failed to download ticket - invalid format');
      }
    } catch (error) {
      console.error('Error downloading ticket:', error);
      alert('Failed to download ticket');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-indigo-500">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{ticket.movie_title}</h3>
          <p className="text-sm text-gray-600">{ticket.theater_name}</p>
        </div>
        <div className="text-right">
          <p className="text-sm font-medium text-indigo-600">#{ticket.ticket_id}</p>
          <p className="text-xs text-gray-500">
            {ticket.created_at ? new Date(ticket.created_at).toLocaleDateString() : 'N/A'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-sm text-gray-600">Show Time</p>
          <p className="font-medium">
            {ticket.showtime}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Seats</p>
          <p className="font-medium">
            {Array.isArray(ticket.seats) ? ticket.seats.join(', ') : 'N/A'}
          </p>
        </div>
      </div>

      <div className="flex justify-between items-center">
        <div>
          <p className="text-sm text-gray-600">Total Amount</p>
          <p className="text-lg font-semibold text-gray-900">
            ${ticket.total_amount}
          </p>
        </div>
        <button
          onClick={handleDownload}
          className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors duration-200 text-sm font-medium"
        >
          Download PDF
        </button>
      </div>
    </div>
  );
};

export default Ticket;
