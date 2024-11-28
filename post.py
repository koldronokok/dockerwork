import psycopg2
from tabulate import tabulate

# Підключення до бази даних
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="cinema_db",
    user="postgres",
    password="root"
)
cur = conn.cursor()


# --- Запит 1: Відобразити всі комедії. Відсортувати фільми по рейтингу ---
print("\n--- Запит 1: Всі комедії, відсортовані по рейтингу ---")
cur.execute("""
    SELECT title, genre, rating
    FROM Movies
    WHERE genre = 'Comedy'
    ORDER BY rating DESC;
""")
comedy_movies = cur.fetchall()
print(tabulate(comedy_movies, headers=["Назва", "Жанр", "Рейтинг"], tablefmt="psql"))

# --- Запит 2: Остання дата показу фільму для кожного транслювання ---
print("\n--- Запит 2: Остання дата показу фільму ---")
cur.execute("""
    SELECT 
        m.title AS "Назва фільму",
        c.name AS "Кінотеатр",
        ms.start_date AS "Дата початку",
        ms.screening_duration AS "Термін показу (днів)",
        ms.start_date + ms.screening_duration * INTERVAL '1 day' AS "Кінцева дата"
    FROM Movie_Screenings ms
    JOIN Movies m ON ms.movie_code = m.movie_code
    JOIN Cinemas c ON ms.cinema_code = c.cinema_code;
""")
last_screening_dates = cur.fetchall()
print(tabulate(last_screening_dates, headers=["Фільм", "Кінотеатр", "Початок", "Тривалість", "Кінець"], tablefmt="psql"))

# --- Запит 3: Максимальний прибуток для кожного кінотеатру ---
print("\n--- Запит 3: Максимальний прибуток для кожного кінотеатру ---")
cur.execute("""
    SELECT 
        c.name AS "Кінотеатр",
        c.ticket_price * c.seats_count AS "Максимальний прибуток за один показ"
    FROM Cinemas c;
""")
max_profit = cur.fetchall()
print(tabulate(max_profit, headers=["Кінотеатр", "Максимальний прибуток"], tablefmt="psql"))

# --- Запит 4: Відобразити всі фільми заданого жанру (запит з параметром) ---
genre = "Action"  # Заданий жанр
print(f"\n--- Запит 4: Всі фільми жанру {genre} ---")
cur.execute("""
    SELECT title, genre, duration, rating
    FROM Movies
    WHERE genre = %s;
""", (genre,))
genre_movies = cur.fetchall()
print(tabulate(genre_movies, headers=["Назва", "Жанр", "Тривалість", "Рейтинг"], tablefmt="psql"))

# --- Запит 5: Кількість фільмів кожного жанру ---
print("\n--- Запит 5: Кількість фільмів кожного жанру ---")
cur.execute("""
    SELECT genre AS "Жанр", COUNT(*) AS "Кількість фільмів"
    FROM Movies
    GROUP BY genre;
""")
movies_per_genre = cur.fetchall()
print(tabulate(movies_per_genre, headers=["Жанр", "Кількість"], tablefmt="psql"))

# --- Запит 6: Кількість фільмів за жанром у кожному кінотеатрі (перехресний запит) ---
print("\n--- Запит 6: Кількість фільмів за жанром у кожному кінотеатрі ---")
cur.execute("""
    SELECT 
        c.name AS "Кінотеатр",
        m.genre AS "Жанр",
        COUNT(*) AS "Кількість"
    FROM Movie_Screenings ms
    JOIN Movies m ON ms.movie_code = m.movie_code
    JOIN Cinemas c ON ms.cinema_code = c.cinema_code
    GROUP BY c.name, m.genre
    ORDER BY c.name, m.genre;
""")
movies_per_genre_per_cinema = cur.fetchall()
print(tabulate(movies_per_genre_per_cinema, headers=["Кінотеатр", "Жанр", "Кількість"], tablefmt="psql"))

# Закриття з'єднання
cur.close()
conn.close()
print("\n--- Виконання завершено! ---")
