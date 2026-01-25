import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Ganti ke SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cinema.db"   # <-- pastikan ini path yang benar
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
