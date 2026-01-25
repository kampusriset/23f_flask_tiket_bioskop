import sqlite3

DB_PATH = "instance/cinema.db"

# Data lengkap film
films_data = [
    {
        "title": "Avengers Endgame",
        "genre": "Action, Sci-Fi",
        "age_rating": "PG-13",
        "duration": "181",
        "director": "Anthony & Joe Russo",
        "cast": "Robert Downey Jr., Chris Evans, Chris Hemsworth, Scarlett Johansson",
        "production": "Marvel Studios",
        "language": "English",
        "description": "Para Avengers yang tersisa berusaha membalikkan kehancuran akibat Thanos dan menyelamatkan alam semesta dalam pertarungan terbesar sepanjang masa."
    },
    {
        "title": "Spider-Man No Way Home",
        "genre": "Action, Adventure, Sci-Fi",
        "age_rating": "PG-13",
        "duration": "148",
        "director": "Jon Watts",
        "cast": "Tom Holland, Zendaya, Benedict Cumberbatch",
        "production": "Marvel Studios",
        "language": "English",
        "description": "Identitas Spider-Man terbongkar dan Peter meminta bantuan Doctor Strange. Mantra gagal dan membuka multiverse, menghadirkan musuh dari dunia lain."
    },
    {
        "title": "Doctor Strange Multiverse of Madness",
        "genre": "Action, Fantasy, Horror",
        "age_rating": "PG-13",
        "duration": "126",
        "director": "Sam Raimi",
        "cast": "Benedict Cumberbatch, Elizabeth Olsen, Xochitl Gomez",
        "production": "Marvel Studios",
        "language": "English",
        "description": "Doctor Strange menghadapi ancaman baru saat menjelajahi multiverse untuk melindungi seorang gadis dengan kekuatan misterius."
    },
    {
        "title": "Guardian of The Galaxy Vol 3",
        "genre": "Action, Comedy, Sci-Fi",
        "age_rating": "PG-13",
        "duration": "149",
        "director": "James Gunn",
        "cast": "Chris Pratt, Zoe Saldaña, Dave Bautista",
        "production": "Marvel Studios",
        "language": "English",
        "description": "Para Guardian melakukan misi besar untuk menyelamatkan Rocket dan mengungkap masa lalunya."
    }
]

def main():
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()

    for film in films_data:
        try:
            c.execute("""
                UPDATE films
                SET genre=?, age_rating=?, duration=?, director=?, cast=?, production=?, language=?, description=?
                WHERE title=?
            """, (
                film["genre"], film["age_rating"], film["duration"], film["director"],
                film["cast"], film["production"], film["language"], film["description"], film["title"]
            ))
            print(f"Updated film: {film['title']}")
        except Exception as e:
            print(f"Failed to update {film['title']} -> {e}")

    db.commit()
    db.close()
    print("Selesai update data film.")

if __name__ == "__main__":
    main()
