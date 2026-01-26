from datetime import datetime
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Film, Schedule, User


def run_seed():
    try:
        # kalau admin sudah ada → jangan seed ulang
        if User.query.filter_by(username="admin").first():
            print("⚠️ Seed sudah pernah dijalankan")
            return
    except OperationalError:
        print("⚠️ Database belum siap")
        return

    # ===== ADMIN =====
    admin = User(
        username="admin",
        password_hash=generate_password_hash("admin123"),
        is_admin=True
    )

    db.session.add(admin)
    db.session.commit()

    print("✅ Admin berhasil di-seed (admin / admin123)")

    # ===== FILM =====
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
            description="Spider-Man NWH"
        ),
        Film(
            title="Doctor Strange: Multiverse of Madness",
            genre="Action, Fantasy",
            duration=126,
            poster="doctor_strange.jpg",
            description="Doctor Strange MOM"
        ),
        Film(
            title="Guardians of the Galaxy Vol. 3",
            genre="Action, Sci-Fi",
            duration=150,
            poster="gotg5.jpg",
            description="GOTG Vol 3"
        ),
    ]

    db.session.add_all(films)
    db.session.commit()

    # ===== SCHEDULE =====
    schedules = [
        Schedule(film_id=films[0].id, show_time=datetime(2026, 2, 1, 18, 30), price=50000),
        Schedule(film_id=films[1].id, show_time=datetime(2026, 2, 2, 20, 0), price=55000),
    ]

    db.session.add_all(schedules)
    db.session.commit()

    print("✅ Film & jadwal berhasil di-seed")
