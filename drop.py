import psycopg2

# Підключення до бази даних
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="clinic_db",
    user="admin",
    password="root"
)
cur = conn.cursor()

# Видалення всіх таблиць
cur.execute("""
    DROP TABLE IF EXISTS Hospitalization, Doctors, Patients CASCADE;
""")
# Використовуємо CASCADE, щоб видалити таблиці та всі залежні від них об'єкти (наприклад, зовнішні ключі)

# Закриваємо підключення
conn.commit()
cur.close()
conn.close()

print("Всі таблиці були видалені успішно!")
