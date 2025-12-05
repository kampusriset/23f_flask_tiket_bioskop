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
