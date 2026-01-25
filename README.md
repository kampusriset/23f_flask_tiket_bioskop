# Flask CGV - Tiket Bioskop

Aplikasi web **Flask CGV** untuk pemesanan tiket bioskop, menampilkan jadwal film, serta mengelola database film dan penonton.

## Fitur

- **Lihat jadwal film**: Menampilkan daftar film dan jam tayang.
- **Pemesanan tiket**: Pilih film, jam tayang, dan lakukan reservasi.
- **Database film & penonton**: CRUD sederhana menggunakan SQLite.
- **Script otomatis**:
  - `generate_schedules.py`: Menghasilkan jadwal film otomatis.
  - `populate_film_details.py`: Mengisi database film awal.
  - `update_films.py` & `update_db.py`: Mengupdate data film dan jadwal.
  - `init_db.py`: Inisialisasi database.
- **Environment virtual**: Menggunakan `venv` untuk dependency isolation.
- **Frontend sederhana**: Menggunakan folder `templates` dan `static`.

## Struktur Folder

flask_cgv/
│
├─ app.py # Main Flask application
├─ requirements.txt # Dependencies
├─ init_db.py # Script inisialisasi database
├─ generate_schedules.py # Generate jadwal film otomatis
├─ populate_film_details.py
├─ update_db.py
├─ update_films.py
├─ instance/ # Database dan konfigurasi lokal
├─ static/ # File statis (CSS, JS, images)
├─ templates/ # Template HTML
└─ venv/ # Virtual environment

## Instalasi

1. Clone repo:
   ```bash
   git clone https://github.com/kampusriset/23f_flask_tiket_bioskop.git
   cd flask_cgv
Buat virtual environment dan aktifkan:

bash
Salin kode
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
Install dependency:

bash
Salin kode
pip install -r requirements.txt
Inisialisasi database:

bash
Salin kode
python init_db.py
python populate_film_details.py
python generate_schedules.py
Jalankan aplikasi:

bash
Salin kode
python app.py
Buka browser dan akses: http://127.0.0.1:5000/

Catatan
Folder instance berisi database lokal (.db).

Pastikan environment virtual aktif saat menjalankan script.

Proyek ini masih menggunakan SQLite untuk database, cocok untuk testing dan development.

Lisensi
MIT License © 2025
