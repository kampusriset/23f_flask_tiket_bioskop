from datetime import datetime
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Film, Schedule, User


def seed_admin():
    try:
        # kalau admin sudah ada, jangan buat ulang
        if User.query.filter_by(username="admin").first():
            return
    except OperationalError:
        return

    admin = User(
        username="admin",
        password_hash=generate_password_hash("admin123"), # AKUN ADMIN
        is_admin=True
    )

    db.session.add(admin)
    db.session.commit()


def seed_films():
    try:
        if Film.query.first():
            return
    except OperationalError:
        return

    films = [
        Film(
            title="Avengers: Endgame",
            genre="Action, Sci-Fi",
            duration=181,
            poster="avengers.jpg",
            description="Avengers Endgame"
        ),
        Film(
            title="Spider-Man: No Way Home",
            genre="Action, Adventure",
            duration=148,
            poster="spiderman.jpg",
            description="Spider-Man No Way Home"
        ),
    ]

    db.session.add_all(films)
    db.session.commit()

    schedules = [
        Schedule(
            film_id=films[0].id,
            show_time=datetime(2026, 2, 1, 13, 0),
            price=40000
        ),
        Schedule(
            film_id=films[1].id,
            show_time=datetime(2026, 2, 2, 15, 0),
            price=45000
        ),
    ]

    db.session.add_all(schedules)
    db.session.commit()


def run_seed():
    seed_admin()
    seed_films()
    print("✅ SEED ADMIN + FILM + JADWAL BERHASIL")
