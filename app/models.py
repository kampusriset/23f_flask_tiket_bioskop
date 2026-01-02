from datetime import datetime
from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    bookings = db.relationship("Booking", back_populates="user", lazy=True)


class Film(db.Model):
    __tablename__ = "films"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    poster = db.Column(db.String(255), nullable=True)
    genre = db.Column(db.String(100), nullable=True, index=True)
    duration = db.Column(db.Integer, nullable=True)

    schedules = db.relationship("Schedule", back_populates="film", lazy=True, cascade="all, delete-orphan")


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("films.id", ondelete="CASCADE"), nullable=False, index=True)
    show_time = db.Column(db.DateTime, nullable=False, index=True)
    price = db.Column(db.Integer, nullable=False, default=0)

    film = db.relationship("Film", back_populates="schedules")
    bookings = db.relationship("Booking", back_populates="schedule", lazy=True)


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False, index=True)
    seats = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    payment_method = db.Column(db.String(50), nullable=True)
    paid_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="bookings")
    schedule = db.relationship("Schedule", back_populates="bookings")
