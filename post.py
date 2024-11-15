import psycopg2
from tabulate import tabulate

# Параметри підключення до БД
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="clinic_db",  # Змініть на вашу базу даних
    user="admin",           # Змініть на вашого користувача
    password="root"         # Змініть на ваш пароль
)
cur = conn.cursor()

# Функція для виводу структури та даних таблиці
def display_table_structure_and_data(table_name):
    # Структура таблиці
    print(f"\n--- Структура таблиці {table_name} ---")
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name.lower()}'")
    structure = cur.fetchall()
    print(tabulate(structure, headers=["Назва колонки", "Тип даних"], tablefmt="psql"))

    # Дані таблиці
    print(f"\n--- Дані таблиці {table_name} ---")
    cur.execute(f"SELECT * FROM {table_name}")
    data = cur.fetchall()
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name.lower()}'")
    headers = [row[0] for row in cur.fetchall()]
    print(tabulate(data, headers=headers, tablefmt="psql"))

# Виведення структури та даних для кожної таблиці
tables = ["patients", "hospitalization", "doctors"]
for table in tables:
    display_table_structure_and_data(table)

# Виконання та вивід запитів
queries = {
    "Пацієнти, народжені після 1998 року": """
        SELECT * FROM patients
        WHERE EXTRACT(YEAR FROM дата_народження) > 1998;
    """,
    "Кількість пацієнтів по категорії": """
        SELECT категорія, COUNT(*) AS кількість
        FROM patients
        GROUP BY категорія;
    """,
    "Кількість звернень до кожного лікаря": """
        SELECT код_лікаря, COUNT(*) AS кількість_звернень
        FROM hospitalization
        GROUP BY код_лікаря;
    """,
    "Кількість пацієнтів кожної категорії за спеціалізацією лікарів": """
        SELECT p.категорія, 
               SUM(CASE WHEN d.спеціалізація = 'лор' THEN 1 ELSE 0 END) AS "ЛОР",
               SUM(CASE WHEN d.спеціалізація = 'терапевт' THEN 1 ELSE 0 END) AS "Терапевт",
               SUM(CASE WHEN d.спеціалізація = 'хірург' THEN 1 ELSE 0 END) AS "Хірург"
        FROM patients p
        JOIN hospitalization h ON p.Номер_карточки_пацієнта = h.Номер_карточки_пацієнта
        JOIN doctors d ON h.код_лікаря = d.код_лікаря
        GROUP BY p.категорія;
    """
}

for description, query in queries.items():
    print(f"\n--- {description} ---")
    try:
        cur.execute(query)
        result = cur.fetchall()
        if result:
            cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{query.split('FROM ')[1].split()[0]}'")
            headers = [row[0] for row in cur.fetchall()]
            print(tabulate(result, headers=headers, tablefmt="psql"))
        else:
            print("Немає даних для відображення.")
    except Exception as e:
        print(f"Помилка виконання запиту: {e}")

cur.close()
conn.close()
