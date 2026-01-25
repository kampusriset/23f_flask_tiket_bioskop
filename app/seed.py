from datetime import datetime
from app.extensions import db
from app.models import Film, Schedule
from sqlalchemy.exc import OperationalError
from app.models import Film, Schedule, User

def seed_data():
    try:
        if User.query.first():
            return
    except OperationalError:
        return

    # ===== SEED ADMIN / DOSEN =====
    admin = User(
        username="dosen",
        password_hash="123456",  #AKUN ADMIN
        is_admin=True
    )

    mahasiswa = User(
        username="mahasiswa",   #AKUN USER
        password_hash="123456",
        is_admin=False
    )

    db.session.add_all([admin, mahasiswa])
    db.session.commit()


def seed_data():
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
            description="""
Avengers: Endgame (2019)

Aktor:
Robert Downey Jr., Chris Evans, Chris Hemsworth, Scarlett Johansson

Setelah Thanos menghapus setengah populasi alam semesta,
Avengers yang tersisa bersatu untuk membalikkan kehancuran
dan mengakhiri perang terbesar sepanjang sejarah.
"""
        ),
        Film(
            title="Spider-Man: No Way Home",
            genre="Action, Adventure",
            duration=148,
            poster="spiderman.jpg",
            description="""
Spider-Man: No Way Home (2021)

Aktor:
Tom Holland, Zendaya, Benedict Cumberbatch

Identitas Peter Parker terbongkar dan membawa kekacauan multiverse
yang mempertemukan musuh-musuh dari dunia lain.
"""
        ),
        Film(
            title="Doctor Strange: Multiverse of Madness",
            genre="Action, Fantasy",
            duration=126,
            poster="doctor_strange.jpg",
            description="""
Doctor Strange in the Multiverse of Madness (2022)

Aktor:
Benedict Cumberbatch, Elizabeth Olsen

Doctor Strange menjelajah multiverse berbahaya
untuk menghadapi ancaman yang belum pernah ada sebelumnya.
"""
        ),
        Film(
            title="Guardians of the Galaxy Vol. 3",
            genre="Action, Sci-Fi",
            duration=150,
            poster="gotg5.jpg",
            description="""
Guardians of the Galaxy Vol. 3 (2023)

Aktor:
Chris Pratt, Zoe Saldana, Dave Bautista

Petualangan terakhir Guardians untuk menyelamatkan Rocket
dan melindungi keluarga yang telah mereka bangun bersama.
"""
        ),
    ]

    db.session.add_all(films)
    db.session.commit()

    schedules = [
        # Avengers
        Schedule(film_id=films[0].id, show_time=datetime(2026, 2, 1, 13, 0), price=40000),
        Schedule(film_id=films[0].id, show_time=datetime(2026, 2, 1, 18, 30), price=50000),

        # Spiderman
        Schedule(film_id=films[1].id, show_time=datetime(2026, 2, 2, 15, 0), price=45000),
        Schedule(film_id=films[1].id, show_time=datetime(2026, 2, 2, 20, 0), price=55000),

        # Doctor Strange
        Schedule(film_id=films[2].id, show_time=datetime(2026, 2, 3, 16, 0), price=45000),
        Schedule(film_id=films[2].id, show_time=datetime(2026, 2, 3, 21, 0), price=55000),

        # Guardians
        Schedule(film_id=films[3].id, show_time=datetime(2026, 2, 4, 14, 0), price=40000),
        Schedule(film_id=films[3].id, show_time=datetime(2026, 2, 4, 19, 30), price=50000),
    ]

    db.session.add_all(schedules)
    db.session.commit()

    print("✅ AUTO SEED 4 FILM + JADWAL + DATA PENONTON BERHASIL")
