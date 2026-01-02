from flask import Blueprint, render_template
from app.models import Film, Schedule
from flask import request, redirect, url_for, flash
from app.extensions import db
from app.models import Film, Schedule, Booking
from datetime import datetime
from flask import request
from flask import Blueprint, render_template, redirect, url_for, flash

# ✅ INI HARUS DI ATAS, SEBELUM @bp.route
bp = Blueprint("public", __name__)

@bp.route("/")
def home():
    q = request.args.get("q", "").strip()

    query = Film.query
    if q:
        query = query.filter(Film.title.ilike(f"%{q}%"))

    films = query.order_by(Film.id.desc()).all()
    featured = films[0] if films else None

    return render_template("index.html", films=films, featured=featured, q=q)

@bp.route("/film/<int:film_id>")
def film_detail(film_id):
    film = Film.query.get_or_404(film_id)

    schedules = (
        Schedule.query
        .filter_by(film_id=film_id)
        .order_by(Schedule.show_time.asc())
        .all()
    )

    return render_template("film_detail.html", film=film, schedules=schedules)
@bp.route("/choose_seat/<int:schedule_id>", methods=["GET", "POST"])
def choose_seat(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    film = Film.query.get_or_404(schedule.film_id)

    # seat yang sudah dibooking untuk jadwal ini
    booked_seats = set()
    for b in Booking.query.filter_by(schedule_id=schedule_id).all():
        for s in (b.seats or "").split(","):
            s = s.strip()
            if s:
                booked_seats.add(s)

    # ✅ repeat order: ambil kursi dari booking lama
    repeat_id = request.args.get("repeat", type=int)
    preselected_seats = []
    if repeat_id:
        old = Booking.query.get_or_404(repeat_id)
        # boleh kamu perketat: pastikan old.user_id == current_user.id
        preselected_seats = [x.strip() for x in (old.seats or "").split(",") if x.strip()]

    if request.method == "POST":
        seats = request.form.get("seats", "").strip()  # "A1,A2"
        if not seats:
            flash("Pilih kursi dulu ya.", "warning")
            return redirect(url_for("public.choose_seat", schedule_id=schedule_id))

        selected = [x.strip() for x in seats.split(",") if x.strip()]
        # validasi: kursi sudah dibooking?
        conflict = [s for s in selected if s in booked_seats]
        if conflict:
            flash(f"Kursi {', '.join(conflict)} sudah dibooking. Pilih yang lain.", "danger")
            return redirect(url_for("public.choose_seat", schedule_id=schedule_id))

        total = len(selected) * (schedule.price or 0)

        # status PENDING, payment_method & paid_at kosong (sesuai kebutuhan kamu)
        from app.models import User  # taruh import ini di atas file kalau belum ada

        user = User.query.order_by(User.id.asc()).first()
        if not user:
            flash("Belum ada user di database. Buat user dulu.", "danger")
            return redirect(url_for("public.home"))

        booking = Booking(
            user_id=user.id,          # ✅ bukan 1 hardcode
            schedule_id=schedule_id,
            seats=",".join(selected),
            total=total,
            status="PENDING"
        )
        db.session.add(booking)
        db.session.commit()


        return redirect(url_for("public.checkout", booking_id=booking.id))

    return render_template(
        "choose_seat.html",
        film=film,
        schedule=schedule,
        booked_seats=sorted(booked_seats),
        preselected_seats=preselected_seats,
        repeat_id=repeat_id
    )
@bp.route("/checkout/<int:booking_id>", methods=["GET", "POST"])
def checkout(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    schedule = Schedule.query.get_or_404(booking.schedule_id)
    film = Film.query.get_or_404(schedule.film_id)

    if request.method == "POST":
        payment_method = request.form.get("payment_method", "").strip()
        paid_at_str = request.form.get("paid_at", "").strip()  # format: YYYY-MM-DD

        booking.payment_method = payment_method or None
        booking.paid_at = datetime.strptime(paid_at_str, "%Y-%m-%d") if paid_at_str else None

        # kalau kamu mau saat checkout langsung dianggap paid:
        booking.status = "PAID" if booking.payment_method and booking.paid_at else "PENDING"

        db.session.commit()
        return redirect(url_for("public.booking_success", booking_id=booking.id))

    return render_template("checkout.html", booking=booking, schedule=schedule, film=film)
@bp.route("/booking/success/<int:booking_id>")
def booking_success(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    schedule = Schedule.query.get_or_404(booking.schedule_id)
    film = Film.query.get_or_404(schedule.film_id)
    return render_template("payment_success.html", booking=booking, schedule=schedule, film=film)
@bp.route("/my_bookings")

def my_bookings():
    # sementara hardcode user_id=1 (nanti ganti ke session user login)
    user_id = 1

    bookings = (
        Booking.query
        .filter_by(user_id=user_id)
        .order_by(Booking.created_at.desc())
        .all()
    )

    # kita siapkan data film + jadwal biar template gampang
    items = []
    for b in bookings:
        schedule = Schedule.query.get(b.schedule_id)
        film = Film.query.get(schedule.film_id) if schedule else None
        items.append({
            "booking": b,
            "schedule": schedule,
            "film": film
        })

    return render_template("my_bookings.html", items=items)