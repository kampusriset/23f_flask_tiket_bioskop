import sqlite3

# Path ke database
DB_PATH = "instance/cinema.db"  # sesuaikan dengan path db-mu

# Kolom yang ingin ditambahkan
columns = [
    ("genre", "TEXT"),
    ("age_rating", "TEXT"),
    ("director", "TEXT"),
    ("cast", "TEXT"),
    ("production", "TEXT"),
    ("language", "TEXT"),
    ("description", "TEXT")
]

def main():
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()

    for col_name, col_type in columns:
        try:
            c.execute(f"ALTER TABLE films ADD COLUMN {col_name} {col_type};")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"Skipped {col_name} -> {e}")

    db.commit()
    db.close()
    print("Selesai update struktur tabel FILMS.")

if __name__ == "__main__":
    main()
