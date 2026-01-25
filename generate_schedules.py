import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("instance/cinema.db")
cur = conn.cursor()

# ambil semua film
cur.execute("SELECT id FROM films")
films = [row[0] for row in cur.fetchall()]

start = datetime(2025, 12, 1)
end = datetime(2025, 12, 31)

def random_showtimes():
    # 3–5 showtime per hari
    show_counts = random.randint(3, 5)
    base_times = ["10:00", "12:30", "15:00", "17:30", "20:00", "22:00"]
    return random.sample(base_times, show_counts)

for film_id in films:
    day = start
    while day <= end:

        for t in random_showtimes():
            show_time = f"{day.date()} {t}"
            price = random.choice([45000, 50000, 55000])

            cur.execute("""
                INSERT INTO schedules (film_id, show_time, price)
                VALUES (?, ?, ?)
            """, (film_id, show_time, price))

        day += timedelta(days=1)

conn.commit()
conn.close()

print("Jadwal sebulan berhasil dibuat!")
