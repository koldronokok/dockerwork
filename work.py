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

# Заповнення таблиці пацієнтів
patients = [
    ('Іванов', 'Іван', 'Іванович', 'Київ, вул. Лесі Українки, 10', '380501234567', 1990, 'доросла'),
    ('Петренко', 'Марія', 'Іванівна', 'Київ, вул. Шевченка, 5', '380502345678', 2000, 'дитяча'),
    ('Ковальчук', 'Олена', 'Анатоліївна', 'Київ, вул. Дніпровська, 15', '380503456789', 1995, 'доросла')
]

for patient in patients:
    cur.execute("""
        INSERT INTO Patients (last_name, first_name, middle_name, address, phone, birth_year, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, patient)

# Заповнення таблиці лікарів
doctors = [
    ('Петров', 'Олександр', 'Васильович', 'терапевт', 10),
    ('Сидоренко', 'Ганна', 'Олександрівна', 'лікар-хірург', 12),
    ('Мельник', 'Анна', 'Миколаївна', 'лор', 8),
    ('Коваленко', 'Володимир', 'Іванович', 'терапевт', 15)
]

for doctor in doctors:
    cur.execute("""
        INSERT INTO Doctors (last_name, first_name, middle_name, specialization, experience)
        VALUES (%s, %s, %s, %s, %s);
    """, doctor)

# Заповнення таблиці прибування в стаціонарі
hospitalizations = [
    (1, '2024-01-10', 5, 1000, 10, 1),
    (2, '2024-02-15', 7, 1200, 5, 2),
    (3, '2024-03-20', 6, 1500, 12, 3),  # Додано пацієнта з patient_id = 3
]

for hospitalization in hospitalizations:
    cur.execute("""
        INSERT INTO Hospitalization (patient_id, admission_date, days_in_hospital, treatment_cost, discount, doctor_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, hospitalization)

# Закриваємо підключення
conn.commit()
cur.close()
conn.close()
print("Дані додано успішно!")
