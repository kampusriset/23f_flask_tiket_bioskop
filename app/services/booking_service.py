from app.models import Booking
from app.extensions import db

def is_seat_taken(schedule_id, selected_seats):
    bookings = Booking.query.filter_by(schedule_id=schedule_id).all()

    booked_seats = set()
    for b in bookings:
        if b.seats:
            booked_seats.update(s.strip() for s in b.seats.split(","))

    return any(seat in booked_seats for seat in selected_seats)


def create_booking(user_id, schedule_id, seats, total):
    try:
        with db.session.begin():
            # 🔒 CEK ULANG DI DALAM TRANSAKSI
            if is_seat_taken(schedule_id, seats):
                raise ValueError("Kursi sudah dibooking")

            booking = Booking(
                user_id=user_id,
                schedule_id=schedule_id,
                seats=",".join(seats),
                total=total,
                status="PENDING"
            )

            db.session.add(booking)

        return booking

    except Exception:
        db.session.rollback()
        raise
