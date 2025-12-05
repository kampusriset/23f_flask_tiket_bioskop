import sqlite3

conn = sqlite3.connect("cinema.db")
cur = conn.cursor()

# ---- TABLE MOVIES ----
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    poster TEXT,
    description TEXT
)
""")

# ---- TABLE SCHEDULES ----
cur.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER,
    show_date TEXT,
    show_time TEXT,
    price INTEGER DEFAULT 35000,
    FOREIGN KEY(movie_id) REFERENCES movies(id)
)
""")

# ---- TABLE USERS ----
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# ---- TABLE BOOKINGS ----
cur.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    schedule_id INTEGER,
    seats TEXT,
    total INTEGER,
    status TEXT DEFAULT 'pending',
    created_at TEXT
)
""")

# ---- INSERT 4 FILM ----
cur.execute("DELETE FROM movies")

movies = [
    ("Avenger End Game", "endgame.jpg", "Film Avengers terbaik."),
    ("Spiderman No Way Home", "spiderman.jpg", "Film Spiderman multiverse."),
    ("Interstellar", "interstellar.jpg", "Film sci-fi luar angkasa."),
    ("Ironman 3", "ironman3.jpg", "Film Ironman melawan Mandarin.")
]

cur.executemany("""
INSERT INTO movies (title, poster, description)
VALUES (?, ?, ?)
""", movies)

conn.commit()
conn.close()

print("cinema.db berhasil dibuat & diisi data film.")
