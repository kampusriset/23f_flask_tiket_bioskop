from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app.extensions import db
from app.models import Film, Schedule
from app.models import Booking
from sqlalchemy import func
import sqlite3
import os

bp = Blueprint("admin", __name__, url_prefix='/admin')

@bp.route("/films/add", methods=["GET", "POST"])
def add_film():
    if request.method == "POST":
        film = Film(
            title=request.form["title"],
            genre=request.form.get("genre"),
            duration=int(request.form.get("duration") or 0),
            poster=request.form.get("poster"),
            description=request.form.get("description")
        )
        db.session.add(film)
        db.session.commit()
        flash("Film berhasil ditambahkan", "success")
        return redirect(url_for("admin.add_film"))

    return render_template("admin/add_film.html")

@bp.route("/schedules/add", methods=["GET", "POST"])
def add_schedule():
    films = Film.query.all()

    if request.method == "POST":
        schedule = Schedule(
            film_id=request.form["film_id"],
            show_time=datetime.strptime(
                request.form["show_time"], "%Y-%m-%dT%H:%M"
            ),
            price=int(request.form["price"])
        )
        db.session.add(schedule)
        db.session.commit()
        flash("Jadwal berhasil ditambahkan", "success")
        return redirect(url_for("admin.add_schedule"))

    return render_template("admin/add_schedule.html", films=films)

@bp.route("/dashboard")
def dashboard():
    total_film = Film.query.count()
    total_booking = Booking.query.count()
    total_paid = Booking.query.filter_by(status="PAID").count()

    recent_bookings = (
        Booking.query
        .order_by(Booking.created_at.desc())
        .limit(5)
        .all()
    )

    total_income = (
        db.session.query(func.sum(Booking.total))
        .filter(Booking.status == "PAID")
        .scalar()
    ) or 0

    return render_template(
        "admin/dashboard.html",   # 🔴 PENTING
        total_film=total_film,
        total_booking=total_booking,
        total_paid=total_paid,
        total_income=total_income,
        recent_bookings=recent_bookings
    )

@bp.route("/films")
def manage_films():
    if not admin_required():
        flash("Akses ditolak", "danger")
        return redirect(url_for("auth.login"))

    films = Film.query.all()
    return render_template("admin/manage_films.html", films=films)

@bp.route("/films/edit/<int:id>", methods=["GET", "POST"])
def edit_film(id):
    film = Film.query.get_or_404(id)

    if request.method == "POST":
        film.title = request.form["title"]
        film.genre = request.form.get("genre")
        film.duration = int(request.form.get("duration") or 0)
        film.poster = request.form.get("poster")
        film.description = request.form.get("description")

        db.session.commit()
        flash("Film berhasil diupdate", "success")
        return redirect(url_for("admin.manage_films"))

    return render_template("admin/edit_film.html", film=film)

@bp.route('/films/delete/<int:id>', methods=['POST'])
def delete_film(id):
    db_path = os.path.join(current_app.instance_path, 'cinema.db')
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM films WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin.manage_films'))
    flash("Film berhasil dihapus", "success")


@bp.route('/schedules')
def manage_schedules():
    if not admin_required():
        flash("Akses ditolak", "danger")
        return redirect(url_for("auth.login"))

    db_path = os.path.join(current_app.instance_path, 'cinema.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT films.title,
               schedules.show_time,
               schedules.price
        FROM schedules
        JOIN films ON schedules.film_id = films.id
        ORDER BY schedules.show_time
    """)
    schedules = cursor.fetchall()
    conn.close()

    return render_template('manage_schedules.html', schedules=schedules)

@bp.route('/reports')
def booking_reports():
    conn = sqlite3.connect('instance/cinema.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bookings.id,
               users.username,
               films.title AS film_title,
               schedules.show_time,
               bookings.seats,
               bookings.total,
               bookings.status,
               bookings.created_at
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN schedules ON bookings.schedule_id = schedules.id
        JOIN films ON schedules.film_id = films.id
        ORDER BY bookings.created_at DESC
    """)

    reports = cursor.fetchall()
    conn.close()

    return render_template('booking_reports.html', reports=reports)

def admin_required():
    if 'username' not in session or session['username'] != 'admin':
        return False
    return True

@bp.route("/bookings")
def manage_bookings():
    bookings = Booking.query.filter(
    Booking.status.in_(["PENDING_PAYMENT", "WAITING_CONFIRMATION"])).all()
    return render_template("manage_bookings.html", bookings=bookings)

@bp.route("/bookings/<int:booking_id>/confirm", methods=["POST"])
def confirm_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = "PAID"
    booking.paid_at = datetime.utcnow()

    db.session.commit()

    flash("Booking berhasil dikonfirmasi", "success")
    return redirect(url_for("admin.manage_bookings"))


@bp.route("/bookings/<int:booking_id>/reject", methods=["POST"])
def reject_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = "REJECTED"

    db.session.commit()

    flash("Booking berhasil ditolak", "danger")
    return redirect(url_for("admin.manage_bookings"))




