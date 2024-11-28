import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="cinema_db",
        user="postgres",
        password="root"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movies (
            movie_code SERIAL PRIMARY KEY,
            title VARCHAR(100),
            genre VARCHAR(50),
            duration INT,
            rating DECIMAL(3,2)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Cinemas (
            cinema_code SERIAL PRIMARY KEY,
            name VARCHAR(100),
            ticket_price DECIMAL(10,2),
            seats_count INT,
            address VARCHAR(255),
            phone VARCHAR(20)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movie_Screenings (
            screening_code SERIAL PRIMARY KEY,
            movie_code INT REFERENCES Movies(movie_code),
            cinema_code INT REFERENCES Cinemas(cinema_code),
            start_date DATE,
            screening_duration INT
        );
    """)

    movies = [
        ("Inception", "Science Fiction", 148, 8.8),
        ("The Hangover", "Comedy", 100, 7.7),
        ("The Notebook", "Romance", 123, 7.8),
        ("Interstellar", "Science Fiction", 169, 8.6),
        ("Joker", "Drama", 122, 8.4),
        ("Avengers: Endgame", "Action", 181, 8.4),
        ("Frozen", "Animation", 102, 7.5),
        ("Parasite", "Thriller", 132, 8.6),
        ("Coco", "Animation", 105, 8.4),
        ("The Godfather", "Crime", 175, 9.2),
        ("The Dark Knight", "Action", 152, 9.0),
    ]

    for movie in movies:
        cur.execute("""
            INSERT INTO Movies (title, genre, duration, rating)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, movie)

    cinemas = [
        ("Cinema City", 10.50, 120, "Kyiv, Maidan Nezalezhnosti, 1", "+380501234567"),
        ("Multiplex", 8.00, 100, "Kyiv, Khreshchatyk St, 25", "+380502345678"),
        ("Oscar", 12.00, 150, "Kyiv, Peremohy Ave, 45", "+380503456789"),
    ]

    for cinema in cinemas:
        cur.execute("""
            INSERT INTO Cinemas (name, ticket_price, seats_count, address, phone)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, cinema)

    screenings = [
        (1, 1, "2024-01-01", 10),
        (2, 1, "2024-01-02", 7),
        (3, 1, "2024-01-03", 5),
        (4, 2, "2024-01-04", 8),
        (5, 2, "2024-01-05", 10),
        (6, 2, "2024-01-06", 12),
        (7, 3, "2024-01-07", 7),
        (8, 3, "2024-01-08", 9),
        (9, 3, "2024-01-09", 6),
        (10, 1, "2024-01-10", 8),
        (11, 2, "2024-01-11", 10),
        (1, 3, "2024-01-12", 7),
        (2, 2, "2024-01-13", 8),
        (3, 1, "2024-01-14", 6),
        (4, 3, "2024-01-15", 9),
    ]

    for screening in screenings:
        cur.execute("""
            INSERT INTO Movie_Screenings (movie_code, cinema_code, start_date, screening_duration)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, screening)

    conn.commit()

    # Виведення вмісту таблиць
    print("\n--- Movies ---")
    cur.execute("SELECT * FROM Movies;")
    for row in cur.fetchall():
        print(row)

    print("\n--- Cinemas ---")
    cur.execute("SELECT * FROM Cinemas;")
    for row in cur.fetchall():
        print(row)

    print("\n--- Movie Screenings ---")
    cur.execute("SELECT * FROM Movie_Screenings;")
    for row in cur.fetchall():
        print(row)

    print("\nДані успішно додано та виведено на екран!")

except Exception as e:
    print(f"Сталася помилка: {e}")

finally:
    # Закриття з'єднання з базою даних
    if conn:
        cur.close()
        conn.close()
