import sqlite3 as sq
from pprint import pprint

# При использовании менеджера контекста для связи и работы с базой данных надо знать, что при этом неявно работают
# такие методы как
# con.commit() - сохраняет все производимые изменения в базу данных, и
# con.close() - закрывает соединение с БД

with sq.connect("cars.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cars")

with sq.connect("cars.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cars ( 
    car_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    model TEXT, 
    price INTEGER )""")

    # con.commit()
    # con.close()

    #  Добавление записей в таблицу в самом простом варианте происходит как ранее описывалось следующим образом:

    cur.execute("INSERT INTO cars VALUES(1, 'Audi', 52642)")
    cur.execute("INSERT INTO cars VALUES(2, 'Mercedes', 57127)")
    cur.execute("INSERT INTO cars VALUES(3, 'Skoda', 9000)")
    cur.execute("INSERT INTO cars VALUES(4, 'Volvo', 29000)")
    cur.execute("INSERT INTO cars VALUES(5, 'Bentley', 35000)")

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    # [(1, 'Audi', 52642),
    #  (2, 'Mercedes', 57127),
    #  (3, 'Skoda', 9000),
    #  (4, 'Volvo', 29000),
    #  (5, 'Bentley', 35000)]

# Однако когда программируют на python данные, как правило, хранятся в коллекциях:


with sq.connect("cars.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cars")

cars = [('Audi', 52642),  # коллекция для ввода данных в таблицу
        ('Mercedes', 57127),
        ('Skoda', 9000),
        ('Volvo', 29000),
        ('Bentley', 35000)]

with sq.connect("cars.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cars ( 
    car_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    model TEXT, 
    price INTEGER )""")
    #  Далее вместо целого ряда строчек с INSERT пишут sql запрос-шаблон следующего вида:

    for car in cars:
        cur.execute("INSERT INTO cars VALUES(NULL, ?, ?)", car)  # по умолчанию вместо ? вставляется cars[0]
        # ('Audi'), а вместо второго ? (52642) и перебираются все элементы коллекции в цикле for

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    # [(1, 'Audi', 52642),
    #  (2, 'Mercedes', 57127),
    #  (3, 'Skoda', 9000),
    #  (4, 'Volvo', 29000),
    #  (5, 'Bentley', 35000)]

#  Так же можно поступить еще проще и вместо цикла for использовать метод executemany. Синтаксис при этом будет:

with sq.connect("cars.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cars")

cars = [('Audi', 52642),  # коллекция для ввода данных в таблицу
        ('Mercedes', 57127),
        ('Skoda', 9000),
        ('Volvo', 29000),
        ('Bentley', 35000)]

with sq.connect("cars.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT,
    price INTEGER )""")

    cur.executemany("INSERT INTO cars VALUES(NULL, ?, ?)", cars)  # по умолчанию вставляет все значения коллекции

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    # [(1, 'Audi', 52642),
    #  (2, 'Mercedes', 57127),
    #  (3, 'Skoda', 9000),
    #  (4, 'Volvo', 29000),
    #  (5, 'Bentley', 35000)]

#  Так же вместо ? могут использоваться именованные параметры:

with sq.connect("cars.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cars")

cars = [('Audi', 52642),  # коллекция для ввода данных в таблицу
        ('Mercedes', 57127),
        ('Skoda', 9000),
        ('Volvo', 29000),
        ('Bentley', 35000)]

with sq.connect("cars.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT,
    price INTEGER )""")

    # cur.executemany("INSERT INTO cars VALUES(NULL, ?, ?)", cars)
    cur.execute("UPDATE cars SET price = :Price WHERE model LIKE 'A%'", {'Price': 0})

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)
