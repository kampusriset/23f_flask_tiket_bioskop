# Aplikasi Tiket Bioskop – Flask  
Tugas UAS Pemrograman Web

## Deskripsi
Aplikasi web berbasis **Flask** untuk pemesanan tiket bioskop.  
Fitur utama:
- Login & register user
- Melihat daftar film dan detail film
- Pemilihan jadwal & kursi
- Pemesanan tiket
- Download **tiket dalam bentuk PDF**
- Dashboard admin (kelola film, jadwal, dan booking)

---

## Teknologi
- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- xhtml2pdf (export tiket PDF)

---
Akun :
Admin : (bisa tanpa register sudah ke seed otomatis)
- Username: admin
- Password: admin123

User (wajib register)
- Username: user
- Password: user
  

## Cara Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/kampusriset/23f_flask_tiket_bioskop.git
cd 23f_flask_tiket_bioskop

###2. Buat Virtual Environment (opsional tapi disarankan)
python -m venv venv


Aktifkan:
  Windows: venv\Scripts\activate
  Linux / Mac: source venv/bin/activate

###3. Install Dependency
  pip install -r requirements.txt

###4. Inisialisasi Database
  python init_db.py


#Jika menggunakan migration:
  flask db upgrade

###5. Jalankan Aplikasi
  python run.py


Akses di browser:
  http://127.0.0.1:5000

Fitur Download Tiket PDF
Aplikasi mendukung export tiket ke PDF menggunakan library:
  xhtml2pdf

Library ini sudah termasuk di requirements.txt.
