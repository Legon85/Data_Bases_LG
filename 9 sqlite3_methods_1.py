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

#  EXECUTEMANY. Так же можно поступить еще проще и вместо цикла for использовать метод executemany. Синтаксис при
#  этом будет:

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

    cur.executemany("INSERT INTO cars VALUES(NULL, ?, ?)", cars)
    cur.execute("UPDATE cars SET price = :Price WHERE model LIKE 'A%'", {'Price': 0})
    # В данном случае :Price является именованным параметром, а в словаре {'Price': 0} ключ является именем
    # этого параметра, а значение ключа 0 как раз будет подставлено вместо него.

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)
    # В результате этого запроса цена автомобилей начинающихся на букву A установится в ноль.

    # [(1, 'Audi', 0),
    # (2, 'Mercedes', 57127),
    # (3, 'Skoda', 9000),
    # (4, 'Volvo', 29000),
    # (5, 'Bentley', 35000)]

#  EXECUTESCRIPT. Используется для записи нескольких sql запросов. Но в нём нельзя использовать шаблоны запросов
#  как было выше описано. И sql запросы в нём записываются так как они есть.

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

    cur.executemany("INSERT INTO cars VALUES(NULL, ?, ?)", cars)
    cur.executescript("""DELETE FROM cars WHERE model LIKE 'A%'; UPDATE cars SET price = price + 1000""")
    # удалить все машины с начальной буквой А и добавить ко всем ценникам 1000:

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

#  Так же можно реализовывать соединение с БД через блок try-except-finally. В данном случае нужно использовать
#  команды con.commit и con.close для сохранения изменений и закрытия базы, поскольку тут мы не используем
#  менеджер контекста with. А так же, в начале sql запроса для записи данных в таблицу, прописывается метка
#  BEGIN. На неё, в случае ошибок в БД, будет произведён откат изменений con.rollback в блоке except.
#  Преимущество данного способа в том что мы обрабатываем случаи с ошибками и откатываем данные. А соединение
#  закрывается в любом случае в блоке finally

con = None
try:
    con = sq.connect("cars.db")
    cur = con.cursor()

    cur.executescript("""DROP TABLE IF EXISTS cars;
        CREATE TABLE IF NOT EXISTS cars (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        price INTEGER
    );   
    BEGIN;  
    INSERT INTO cars VALUES(1, 'Audi', 52642);
    INSERT INTO cars VALUES(2, 'Mercedes', 57127);
    INSERT INTO cars VALUES(3, 'Skoda', 9000);
    INSERT INTO cars VALUES(4, 'Volvo', 29000);
    INSERT INTO cars VALUES(5, 'Bentley', 35000);
    UPDATE cars SET price = price + 1000;
    """)
    con.commit()  # сохранение изменений
except sq.Error as e:  # в случае ошибки ...
    if con: con.rollback()  # откатываем все изменения до метки BEGIN
    print("Ошибка выполнения запроса")
finally:  # выполняется в любом случае закрытие базы данных
    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)  # выводим данные таблицы после запроса
    if con: con.close()  # закрытие соединения с базой

    # [(1, 'Audi', 53642),
    #  (2, 'Mercedes', 58127),
    #  (3, 'Skoda', 10000),
    #  (4, 'Volvo', 30000),
    #  (5, 'Bentley', 36000)]

#  Для примера искусственно создадим ошибку в запросе (поставим cars2 вместо cars) и убедимся что данные откатятся
#  на метку BEGIN. И таблица в данном случае останется пустой, а мы получим сообщение "ошибка выполнения запроса"

con = None
try:
    con = sq.connect("cars.db")
    cur = con.cursor()

    cur.executescript("""DROP TABLE IF EXISTS cars;
        CREATE TABLE IF NOT EXISTS cars (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        price INTEGER
    );   
    BEGIN;  
    INSERT INTO cars VALUES(1, 'Audi', 52642);
    INSERT INTO cars VALUES(2, 'Mercedes', 57127);
    INSERT INTO cars VALUES(3, 'Skoda', 9000);
    INSERT INTO cars VALUES(4, 'Volvo', 29000);
    INSERT INTO cars VALUES(5, 'Bentley', 35000);
    UPDATE cars2 SET price = price + 1000;
    """)
    con.commit()  # сохранение изменений
except sq.Error as e:  # в случае ошибки ...
    if con: con.rollback()  # откатываем все изменения до метки BEGIN
    print("Ошибка выполнения запроса")
finally:  # выполняется в любом случае закрытие базы данных
    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)  # выводим данные таблицы после запроса
    if con: con.close()  # закрытие соединения с базой

    # Ошибка выполнения запроса
    # []

#  Задача: Предположим при покупке машин в трейд-ин сданная машина записывается в конец таблицы cars,
#  а в новую таблицу cust записывается фамилия владельца id сданной машины и id новой купленной машины. Надо
#  написать программу выполнения sql-запросов для данной задачи.

with sq.connect("cars.db") as con:
    cur = con.cursor()

    # создадим 2 таблицы cars , cast:
    cur.executescript("""DROP TABLE IF EXISTS cars;
    CREATE TABLE IF NOT EXISTS cars (
    car_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT,
    price INTEGER );
    INSERT INTO cars VALUES(1, 'Audi', 52642);
    INSERT INTO cars VALUES(2, 'Mercedes', 57127);
    INSERT INTO cars VALUES(3, 'Skoda', 9000);
    INSERT INTO cars VALUES(4, 'Volvo', 29000);
    INSERT INTO cars VALUES(5, 'Bentley', 35000);
    UPDATE cars SET price = price + 1000;
    DROP TABLE IF EXISTS cust;
    CREATE TABLE IF NOT EXISTS cust(name TEXT, tr_in INTEGER, by INTEGER);
    """)

    # добавим в конец таблицы cars запись о сданном в трейд-ин авто:
    cur.execute("INSERT INTO cars VALUES(NULL, 'Запорожец', 1000)")

    last_row_id = cur.lastrowid  # !!!Здесь свойство lastrowid содержит id последней записи в таблице cars!!!
    buy_car_id = 2  # это, допустим, id нового купленного авто
    cur.execute("INSERT INTO cust VALUES('Фёдор',?,?)", (last_row_id, buy_car_id))
    # здесь мы пользуемся
    # шаблоном для вставления значений находящихся в коллекции (last_row_id, buy_car_id) где у нас фамилия, id
    # сданного авто и нового купленного авто
