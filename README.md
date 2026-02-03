# Nama Aplikasi  
Sistem Pembelian & Kelola Film Tiket Bioskop

## Deskripsi Aplikasi
Aplikasi web berbasis **Flask** untuk pemesanan tiket bioskop.  
Fitur utama:
- Login & register user
- Melihat daftar film dan detail film
- Pemilihan jadwal & kursi
- Pemesanan tiket
- Download **tiket dalam bentuk PDF**
- Dashboard admin (kelola film, jadwal, dan booking)

---
## Flowchart Sistem

---
## Akun 
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
```
---

### 2. Buat Virtual Environment (opsional tapi disarankan)
```bash
python -m venv venv


Windows    : venv\Scripts\activate
Linux / Mac: source venv/bin/activate
```
---

### 3. Install Dependency
```bash
pip install -r requirements.txt
```
---

### 4. Inisialisasi Database
```bash
flask shell


from app.extensions import db
db.create_all()
exit()
```
---


### 5. Jalankan Aplikasi
```bash
flask run
```
---

### Login Akun :
```bash
(User): wajib registrasi 
(Admin): 
username: admin
password: admin123 (sudah seed otomatis)
```

Akses di browser:
```bash
http://127.0.0.1:5000
```
---

Fitur Download Tiket PDF
Aplikasi mendukung export tiket ke PDF menggunakan library:
  xhtml2pdf

Library ini sudah termasuk di requirements.txt.
