from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app.extensions import db
from app.models import Film, Schedule, Booking, User
from app.services.booking_service import is_seat_taken, create_booking
from flask import render_template, make_response
from xhtml2pdf import pisa
from io import BytesIO


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
        seats = request.form.get("seats", "").strip()
        selected = [x.strip() for x in seats.split(",") if x.strip()]

        if is_seat_taken(schedule_id, selected):
            flash("Kursi sudah dibooking.", "danger")
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
            status="WAITING_CONFIRMATION",
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
    # 🔒 HARUS LOGIN
    if "user_id" not in session:
        flash("Silakan login terlebih dahulu untuk checkout.", "warning")
        return redirect(url_for("auth.login"))

    # 🚫 ADMIN TIDAK BOLEH CHECKOUT
    if session.get("is_admin"):
        flash("Admin tidak diperbolehkan melakukan checkout.", "danger")
        return redirect(url_for("public.home"))

    booking = Booking.query.get_or_404(booking_id)

    # 🔐 USER HANYA BOLEH CHECKOUT BOOKING MILIK SENDIRI
    if booking.user_id != session.get("user_id"):
        flash("Anda tidak memiliki akses ke booking ini.", "danger")
        return redirect(url_for("public.home"))

    schedule = Schedule.query.get_or_404(booking.schedule_id)
    film = Film.query.get_or_404(schedule.film_id)

    if request.method == "POST":
        booking.payment_method = request.form.get("payment_method")
        booking.paid_at = None
        booking.status = "WAITING_CONFIRMATION"

        db.session.commit()
        return redirect(url_for("public.booking_success", booking_id=booking.id))

    return render_template(
        "checkout.html",
        booking=booking,
        schedule=schedule,
        film=film
    )



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

@bp.route("/ticket/<int:booking_id>")
def ticket_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # pengaman: cuma booking PAID yang boleh dilihat
    if booking.status != "PAID":
        flash("Tiket belum tersedia", "warning")
        return redirect(url_for("public.my_bookings"))

    return render_template(
        "ticket_detail.html",
        booking=booking
    )

@bp.route("/ticket/<int:booking_id>/pdf")
def ticket_pdf(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    html = render_template(
        "ticket_pdf.html",
        booking=booking
    )

    result = BytesIO()
    pisa.CreatePDF(html, dest=result)

    response = make_response(result.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f"inline; filename=ticket-{booking.id}.pdf"
    )

    return response
