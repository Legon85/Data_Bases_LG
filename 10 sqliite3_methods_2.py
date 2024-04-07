import sqlite3 as sq
from pprint import pprint

# Способы извлечения данных из запросов:
# fetchall() - возвращает число записей в виде упорядоченного списка
# fetchmany(size) - возвращает число записей не более size
# fetchone() - возвращает первую запись


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

    for car in cars:
        cur.execute("INSERT INTO cars VALUES(NULL, ?, ?)", car)

    cur.execute("SELECT * FROM cars ")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    # Что на python получить доступ к выборке типа:
    cur.execute("SELECT model, price FROM cars")
# как раз и используются методы fetch:

# разблокировать для проверки!
# rows = cur.fetchall()
# pprint(rows, indent=0, width=20)
# print("--" * 40)

# [('Audi', 52642),
#  ('Mercedes', 57127),
#  ('Skoda', 9000),
#  ('Volvo', 29000),
#  ('Bentley', 35000)]

#  Остальные разблокировать для проверки

# rows = cur.fetchone()
# pprint(rows, indent=0, width=20)
# print("--" * 40)

# ('Audi', 52642)

# rows = cur.fetchmany(4)
# pprint(rows,indent=0, width=20)
# print("--" * 40)

# [('Audi', 52642),
#  ('Mercedes', 57127),
#  ('Skoda', 9000),
#  ('Volvo', 29000)]


#  Так же сам экземпляр выборки cur.execute("SELECT model, price FROM cars") можно перебирать в цикле:
# разблокировать для проверки!
# for result in cur:
#     print(result)

# Преимущество этого в экономии памяти. т.к. для каждой итерации цикла хранится в памяти только одна запись.

# Вместо вывода кортежей можно выводить пары словаря ключ - значение. Для этого перед созданием таблицы нужно
# указать синтаксис вида  con.row_factory = sq.Row и вывести данные  result['model'], result['price']

cars = [('Audi', 52642),  # коллекция для ввода данных в таблицу
        ('Mercedes', 57127),
        ('Skoda', 9000),
        ('Volvo', 29000),
        ('Bentley', 35000)]

with sq.connect("cars.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cars ( 
        car_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        model TEXT, 
        price INTEGER )
    """)

    cur.execute("SELECT model, price FROM cars")

    for result in cur:
        print(result['model'], result['price'])

    # Audi 52642
    # Mercedes 57127
    # Skoda 9000
    # Volvo 29000
    # Bentley 35000

    #  Способ хранения изображений в БД. Создадим таблицу, которая будет содержать поле ava с типом данных BLOB(
    #  данные в бинарном виде, никак не преобразованные)


def readAva(n):
    """Функция чтения аватарок из каталога  avas в бинарном режиме"""
    try:
        with open(f"avas/{n}.jpg", "rb") as f:
            return f.read()
    except IOError as e:
        print(e)  # в случае ошибки выводится е и False
        return False


def writeAva(name, data):
    """Функция записи аватарок из бинарного режима в графический"""
    try:
        with open(name, "wb") as f:  # открываем файл на запись в бинарном режиме
            f.write(data)  # записываем данные
    except IOError as e:
        print(e)
        return False
    return True


with sq.connect("cars.db") as con:
    con.row_factory = sq.Row
    cur = con.cursor()

    cur.executescript("""DROP TABLE IF EXISTS users;
    CREATE TABLE IF NOT EXISTS users ( 
        name TEXT, 
        ava BLOB, 
        score INTEGER )
    """)

    # Данные изображений могут записываться в БД только в виде специального бинарного объекта sq.Binary().
    # Поэтому прочитаем наше изображение с помощью выше объявленной функции  readAva() , запишем в переменную
    # img и преобразуем в этот бинарный объект sq.Binary(img). А далее уже с помощью шаблона sql вставим его в
    # таблицу:
    img = readAva(1)
    if img:
        binary = sq.Binary(img)
        cur.execute("INSERT INTO users VALUES('Николай', ?, 1000)", (binary,))
    # На данном этапе бинарные данные(картинка) записана в БД.
    # Теперь прочитаем картинку из БД следующим образом:
    cur.execute("SELECT ava FROM users LIMIT 1")
    img = cur.fetchone()['ava']
    # В данном случае обращаемся по ключу т.к. перед соединением с БД у нас было
    # прописано использование словаря - con.row_factory = sq.Row. В противном случае надо было бы обращаться по
    # индексу. Но чтобы убедиться, что мы правильно прочитали данные, нужно объявить функцию writeAva() - см.выше,
    # которая будет выводить эти данные в виде графического файла и передадим ей параметры out.jpg - имя
    # записываемого файла и img - сам файл
    writeAva("out.jpg", img)
    #  на выходе получаем графический файл в нашем каталоге с именем out.jpg, который соответствует тому, что был
    #  записан ранее в БД

#  iterdump() - это метод класса курсор, возвращающий итератор для sql запросов, на основе которых можно
#  воссоздавать текущую базу данных.
#  Имея в наличии, например нашу базу данных cars.db, при помощи iterdump и цикла for можно получить список sql
#  запросов для формирования таблиц этой базы данных

with sq.connect("cars.db") as con:
    cur = con.cursor()

    # for sql in con.iterdump():
    #     print(sql)

    #  Что бы программа выглядела более функциональной запишем все эти запросы в файл:
    # with open("sql_dump.sql", "w") as f:
    #     for sql in con.iterdump():
    #         f.write(sql)
# #  Теперь в нашем каталоге есть файл sql_dump.sql содержащий в себе  конструкции sql с помощью которых мы можем
#  воссоздать таблицы базы данных.
#  Теперь специально удалим базу данных cars.db и попробуем её восстановить с помощью sql_dump.sql
#  Для этого откроем этот файл на чтение и с помощью executescript() восстановим базу:
#     раскомментировать для проверки:
#     with open("sql_dump.sql", "r") as f:
#         sql = f.read()
#         cur.executescript(sql)

# Ещё одной особенностью модуля sqlite является возможность создания базы данных непросредственно в памяти для
# временного хранения таблиц и реализации запросов к ним. Для этого используется конструкция вида:
# con = sq.connect(':memory:')
# и в остальном с ней можно работать так же как в обычном случае,
# когда мы записываем базу данных на диск
