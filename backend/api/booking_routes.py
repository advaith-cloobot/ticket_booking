from flask import Blueprint, request, jsonify, current_app, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Booking, BookedSeat, Showtime, User
from sqlalchemy import and_
from datetime import datetime, timedelta
import uuid
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

booking_bp = Blueprint('booking', __name__)

def generate_ticket_id():
    return str(uuid.uuid4())[:8].upper()

@booking_bp.route('/book/initiate', methods=['POST'])
@jwt_required()
def initiate_booking():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data or not data.get('showtime_id') or not data.get('seats'):
            return jsonify({'error': 'Showtime ID and seats are required'}), 400
        
        showtime = Showtime.query.get(data['showtime_id'])
        if not showtime:
            return jsonify({'error': 'Showtime not found'}), 404
        
        # Check if seats are already booked
        seats = data['seats']
        for seat in seats:
            existing_booking = BookedSeat.query.join(Booking).filter(
                and_(
                    BookedSeat.seat_id == seat,
                    Booking.showtime_id == data['showtime_id'],
                    Booking.booking_status.in_(['pending', 'confirmed'])
                )
            ).first()
            
            if existing_booking:
                return jsonify({'error': f'Seat {seat} is already booked'}), 400
        
        # Calculate total amount
        total_amount = len(seats) * float(showtime.ticket_price)
        
        # Create booking
        booking = Booking(
            user_id=user_id,
            showtime_id=data['showtime_id'],
            ticket_id=generate_ticket_id(),
            total_amount=total_amount,
            booking_status='pending'
        )
        
        db.session.add(booking)
        db.session.flush()  # Get the booking ID
        
        # Create booked seats
        for seat in seats:
            booked_seat = BookedSeat(
                booking_id=booking.id,
                seat_id=seat
            )
            db.session.add(booked_seat)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking initiated successfully',
            'booking_id': booking.id,
            'ticket_id': booking.ticket_id,
            'total_amount': float(total_amount),
            'seats': seats
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/book/payment', methods=['POST'])
@jwt_required()
def process_payment():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data or not data.get('booking_id'):
            return jsonify({'error': 'Booking ID is required'}), 400
        
        booking = Booking.query.filter_by(id=data['booking_id'], user_id=user_id).first()
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        if booking.booking_status != 'pending':
            return jsonify({'error': 'Booking is not in pending status'}), 400
        
        # Process payment (simplified - just update booking status)
        booking.booking_status = 'confirmed'
        booking.payment_status = 'paid'
        booking.payment_method = data.get('payment_method', 'card')
        booking.payment_reference = data.get('payment_reference', f'PAY_{booking.ticket_id}')
        booking.confirmed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment processed successfully',
            'booking_id': booking.id,
            'ticket_id': booking.ticket_id,
            'status': 'confirmed'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/my-tickets', methods=['GET'])
@jwt_required()
def get_my_tickets():
    try:
        user_id = get_jwt_identity()
        
        bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
        
        tickets = []
        for booking in bookings:
            showtime = Showtime.query.get(booking.showtime_id)
            if showtime:
                movie = showtime.movie
                theater = showtime.theater
                
                # Get booked seats
                booked_seats = [seat.seat_id for seat in booking.booked_seats]
                
                ticket = {
                    'id': booking.id,
                    'ticket_id': booking.ticket_id,
                    'movie_title': movie.title,
                    'theater_name': theater.name,
                    'showtime': showtime.show_time.strftime('%Y-%m-%d %H:%M'),
                    'seats': booked_seats,
                    'total_amount': float(booking.total_amount),
                    'status': booking.booking_status,
                    'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M')
                }
                tickets.append(ticket)
        
        return jsonify({'tickets': tickets}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/ticket/<ticket_id>/download', methods=['GET'])
@jwt_required()
def download_ticket(ticket_id):
    try:
        user_id = get_jwt_identity()
        
        booking = Booking.query.filter_by(ticket_id=ticket_id, user_id=user_id).first()
        if not booking:
            return jsonify({'error': 'Ticket not found'}), 404
        
        if booking.booking_status != 'confirmed':
            return jsonify({'error': 'Ticket not confirmed'}), 400
        
        showtime = Showtime.query.get(booking.showtime_id)
        movie = showtime.movie
        theater = showtime.theater
        booked_seats = [seat.seat_id for seat in booking.booked_seats]
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph("🎬 MOVIE TICKET", title_style))
        story.append(Spacer(1, 20))
        
        # Ticket details
        ticket_data = [
            ['Ticket ID:', booking.ticket_id],
            ['Movie:', movie.title],
            ['Theater:', theater.name],
            ['Show Time:', showtime.show_time.strftime('%Y-%m-%d %H:%M')],
            ['Seats:', ', '.join(booked_seats)],
            ['Total Amount:', f'${float(booking.total_amount):.2f}'],
            ['Booking Date:', booking.created_at.strftime('%Y-%m-%d %H:%M')],
            ['Status:', 'CONFIRMED']
        ]
        
        # Create table
        table = Table(ticket_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,  # Center alignment
            textColor=colors.grey
        )
        story.append(Paragraph("Thank you for choosing Movie Tickets!", footer_style))
        story.append(Paragraph("Please arrive 15 minutes before showtime", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        buffer.seek(0)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Create response
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=ticket_{booking.ticket_id}.pdf'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500