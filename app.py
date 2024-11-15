import psycopg2

# Підключення до БД
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="clinic_db",
    user="admin",
    password="root"
)
cur = conn.cursor()

# Створення таблиць
cur.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        patient_id SERIAL PRIMARY KEY,
        last_name VARCHAR(50),
        first_name VARCHAR(50),
        middle_name VARCHAR(50),
        address TEXT,
        phone VARCHAR(15),
        birth_year INT,
        category VARCHAR(20)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Hospitalization (
        hospitalization_id SERIAL PRIMARY KEY,
        patient_id INT REFERENCES Patients(patient_id),
        admission_date DATE,
        days_in_hospital INT,
        treatment_cost DECIMAL(10, 2),
        discount DECIMAL(5, 2),
        doctor_id INT,
        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS Doctors (
        doctor_id SERIAL PRIMARY KEY,
        last_name VARCHAR(50),
        first_name VARCHAR(50),
        middle_name VARCHAR(50),
        specialization VARCHAR(50),
        experience INT
    );
""")

# Закриваємо підключення
conn.commit()
cur.close()
conn.close()

print("Таблиці створено успішно!")
