import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="cinema_db", 
    user="postgres",
    password="root"
)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS Movie_Screenings, Cinemas, Movies CASCADE;
""")

conn.commit()
cur.close()
conn.close()

print("Всі таблиці були видалені успішно!")
