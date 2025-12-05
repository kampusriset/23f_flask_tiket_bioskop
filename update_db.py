import sqlite3

con = sqlite3.connect("instance/cinema.db")
cur = con.cursor()

columns = [
    "genre TEXT",
    "director TEXT",
    "actors TEXT",
    "rating TEXT",
    "sinopsis TEXT",
    "studio TEXT",
    "distributor TEXT",
    "release_date TEXT"
]

for col in columns:
    try:
        cur.execute(f"ALTER TABLE films ADD COLUMN {col};")
        print(f"Added: {col}")
    except Exception as e:
        print(f"Skip {col} -> {e}")

con.commit()
con.close()
