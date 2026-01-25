DATABASE = "cinema.db"
import qrcode
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'change-this-secret'
DATABASE = os.path.join('instance', 'cinema.db')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Silakan login terlebih dahulu untuk melanjutkan.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.before_request
def update_marvel_movies():
    db = get_db()

    marvel_detail = {
        "Avengers Endgame": {
            "duration": "3 jam 1 menit",
            "poster": "/static/posters/endgame.jpg",
            "description": """
Genre: Action, Sci-Fi
Rating: PG-13
Rilis: 2019
Sutradara: Anthony & Joe Russo
Pemeran: Robert Downey Jr., Chris Evans, Chris Hemsworth, Scarlett Johansson

Sinopsis:
Para Avengers yang tersisa berusaha membalikkan kehancuran akibat Thanos dan
menyelamatkan alam semesta dalam pertarungan terbesar sepanjang masa.
"""
        },
        "Spider-Man No Way Home": {
            "duration": "2 jam 28 menit",
            "poster": "/static/posters/spiderman.jpg",
            "description": """
Genre: Action, Adventure, Sci-Fi
Rating: PG-13
Rilis: 2021
Sutradara: Jon Watts
Pemeran: Tom Holland, Zendaya, Benedict Cumberbatch

Sinopsis:
Identitas Spider-Man terbongkar dan Peter meminta bantuan Doctor Strange.
Mantra gagal dan membuka multiverse, menghadirkan musuh dari dunia lain.
"""
        },
        "Doctor Strange Multiverse of Madness": {
            "duration": "2 jam 6 menit",
            "poster": "/static/posters/drstrange2.jpg",
            "description": """
Genre: Action, Fantasy, Horror
Rating: PG-13
Rilis: 2022
Sutradara: Sam Raimi
Pemeran: Benedict Cumberbatch, Elizabeth Olsen, Xochitl Gomez

Sinopsis:
Doctor Strange menghadapi ancaman baru saat menjelajahi multiverse
untuk melindungi seorang gadis dengan kekuatan misterius.
"""
        },
        "Guardian of The Galaxy Vol 3": {
            "duration": "2 jam 29 menit",
            "poster": "/static/posters/gotg3.jpg",
            "description": """
Genre: Action, Comedy, Sci-Fi
Rating: PG-13
Rilis: 2023
Sutradara: James Gunn
Pemeran: Chris Pratt, Zoe Saldaña, Dave Bautista

Sinopsis:
Para Guardian melakukan misi besar untuk menyelamatkan Rocket
dan mengungkap masa lalunya.
"""
        }
    }

    for title, data in marvel_detail.items():
        db.execute("""
            UPDATE films
            SET duration=?, description=?, poster=?
            WHERE title=?
        """, (data["duration"], data["description"], data["poster"], title))

    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def generate_qr(booking_id, total_price):
    data = f"PAYMENT | BOOKING={booking_id} | AMOUNT={total_price}"
    img = qrcode.make(data)

    qr_path = f"static/qr/{booking_id}.png"
    img.save(qr_path)

    return qr_path



# ----------------------- HOME -----------------------
@app.route('/')
def index():
    db = get_db()
    films = db.execute('SELECT * FROM films').fetchall()
    return render_template('index.html', films=films)


@app.route('/films')
def films():
    db = get_db()
    films = db.execute('SELECT * FROM films').fetchall()
    return render_template('films.html', films=films)


# ----------------------- FILM DETAIL -----------------------
@app.route('/film/<int:film_id>')
def film_detail(film_id):
    db = get_db()
    film = db.execute('SELECT * FROM films WHERE id=?', (film_id,)).fetchone()

    dates = db.execute("""
        SELECT DISTINCT substr(show_time, 1, 10) AS date
        FROM schedules
        WHERE film_id = ?
        ORDER BY date
    """, (film_id,)).fetchall()

    return render_template('film_detail.html', film=film, dates=dates)


@app.route('/film/<int:film_id>/schedule')
def film_schedule_by_date(film_id):
    selected_date = request.args.get("date")
    db = get_db()

    schedules = db.execute("""
        SELECT id, show_time, price
        FROM schedules
        WHERE film_id=? AND substr(show_time,1,10)=?
        ORDER BY show_time ASC
    """, (film_id, selected_date)).fetchall()

    data = []
    for s in schedules:
        tgl, jam = s["show_time"].split(" ")
        data.append({
            "id": s["id"],
            "time": jam,
            "price": s["price"]
        })

    return jsonify(data)

# ----------------------- choose seat -----------------------

@app.route('/choose_seat/<int:schedule_id>')
@login_required
def choose_seat(schedule_id):
    db = get_db()

    # Ambil data kursi yang sudah dibooking
    booked = db.execute("""
        SELECT seats FROM bookings
        WHERE schedule_id=? AND status!='canceled'  
    """, (schedule_id,)).fetchall()

    booked_seats = []
    for b in booked:
        if b["seats"]:
            booked_seats.extend(b["seats"].split(","))

    return render_template("choose_seat.html",
                           schedule_id=schedule_id,
                           booked=booked_seats)



# ----------------------- AUTH -----------------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (username,password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            flash('Register sukses. Silakan login.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username mungkin sudah dipakai.', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        user = db.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            flash('Login sukses', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login gagal', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))


# ----------------------- CHECKOUT -----------------------
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    schedule_id = request.form['schedule_id']
    seats = request.form.get('seats')
    user_id = session.get('user_id')

    db = get_db()
    sch = db.execute('SELECT * FROM schedules WHERE id=?', (schedule_id,)).fetchone()

    seat_list = seats.split(',') if seats else []
    total = len(seat_list) * sch['price']

    db.execute(
        'INSERT INTO bookings (user_id,schedule_id,seats,total,status,created_at) VALUES (?,?,?,?,?,?)',
        (user_id, schedule_id, seats, total, 'pending', datetime.utcnow().isoformat())
    )
    db.commit()

    booking_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    return render_template(
        "checkout.html",
        booking_id=booking_id,
        seats=seat_list,
        total_price=total
    )




# ----------------------- PAY BOOKING ID -----------------------

@app.route('/pay/<booking_id>', methods=['POST'])
@login_required
def pay(booking_id):
    db = get_db()
    cur = db.cursor()

    # Ambil data booking
    cur.execute("SELECT seats, total FROM bookings WHERE id=?", (booking_id,))
    data = cur.fetchone()

    if not data:
        return "Booking tidak ditemukan", 404

    seats = data["seats"].split(",") if data["seats"] else []
    total_price = data["total"]

    # UPDATE status menjadi paid
    db.execute("UPDATE bookings SET status='WAITING_CONFIRMATION' WHERE id=?", (booking_id,))
    db.commit()

    return render_template("payment_success.html",
                           booking_id=booking_id,
                           seats=seats,
                           total_price=total_price)





# ----------------------- ADMIN -----------------------
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Admin only', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    films = db.execute('SELECT * FROM films').fetchall()
    schedules = db.execute(
        'SELECT s.*, f.title FROM schedules s JOIN films f ON s.film_id=f.id'
    ).fetchall()

    return render_template('admin_dashboard.html', films=films, schedules=schedules)


@app.route('/admin/manage_films', methods=['GET','POST'])
def manage_films():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Admin only', 'danger')
        return redirect(url_for('index'))

    db = get_db()
    if request.method == 'POST':
        title = request.form['title']
        duration = request.form['duration']
        desc = request.form['description']
        poster = request.form.get('poster','/static/img/default.jpg')

        db.execute(
            'INSERT INTO films (title,duration,description,poster) VALUES (?,?,?,?)',
            (title, duration, desc, poster)
        )
        db.commit()

        flash('Film ditambahkan', 'success')
        return redirect(url_for('manage_films'))

    films = db.execute('SELECT * FROM films').fetchall()
    return render_template('manage_films.html', films=films)


# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
