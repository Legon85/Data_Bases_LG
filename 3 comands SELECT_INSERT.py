from pprint import pprint
import sqlite3 as sq

# SQL запросы для добавления данных в таблицу и для выборки данных из таблицы

# INSERT - добавление записи в таблицу
# SELECT - выборка данных из таблицы (в том числе и при создании сводной выборки из нескольких таблиц)

# синтаксисы для добавления записи:

# INSERT INTO<table_name>(<column_name1>,<column_name2>...) VALUES(<value1>,<value2>,...)

# если не указывать поля, то будет подразумеваться, что будем записывать все значения во все поля по порядку
# INSERT INTO<table_name>VALUES(<value1>,<value2>,...)
# Например: INSERT INTO users VALUES('Михаил',1,19,1000)
# либо так: INSERT INTO users (name, old, score)VALUES('Фёдор', 32, 200) Поскольку поле sex имеет ограничитель
# DEFAULT 1 то его можно не указывать в перечне полей и указать только (name, old, score)

# Синтаксис для выборки записей:
# SELECT col1,col2...FROM<table_name>  например: SELECT name,old,score FROM users - будут выведены все поля кроме
# sex
# Для вывода всех имеющихся полей используем * :  SELECT * FROM users

# Но обычно SELECT используют с ключевым словом WHERE, которое определяет условие выборки:
# SELECT col1,col2...FROM<table_name> WHERE<условие> например: SELECT col1,col2...FROM<table_name> WHERE score < 1000
# можно использовать для условия WHERE следующие условия =,==,<,<=,>,>=,!=,BETWEEN,
# например: SELECT * from users WHERE score BETWEEN 500 and 1000 или  SELECT * from users WHERE score == 200

# Но в практике программирования часто при описании фильтра требуется учитывать значения сразу нескольких столбцов.
# Для этого необходимо использовать составные условия.
# Например, нам надо выбрать игроков старше 20 лет и с числом очков менее 1000
# В данных случаях используются следующие ключевые слова:

# AND - условное И: exp1 AND exp2. Истинно, если одновременно истинны exp1 и exp2.
# OR - условное ИЛИ: exp1 OR exp2. Истинно, если истинно exp1 или exp2 или оба выражения.
# NOT - условное НЕ: NOT exp. Преобразует ложное условие в истинное и, наоборот,истинное-в ложное.
# IN - вхождение во множество значений: col IN(val,val2,...)
# NOT IN - не вхождение во множество значений: col NOT IN(val,val2,...)

# Например: SELECT * FROM users WHERE old > 20 AND score < 1000
# SELECT * FROM users WHERE old IN(19,32) AND score < 1000
# SELECT * FROM users WHERE old IN(19,32) AND score < 1000 OR sex = 1 (в данно случае приоритет операции AND выше OR
# и сначала выполняется сравнение AND. Если приоритет требуется поменять то нужно приоритетную операцию проставить в
# скобки: SELECT * FROM users WHERE old IN(19,32) AND (score < 1000 OR sex = 1). Самый же высокий приоритет имеет
# оператор NOT при его наличии.

# Дополнительно к SELECT можно прописать оператор ORDER BY для сортировки по указанному столбцу:

# SELECT * FROM users
# WHERE old IN(19,32) AND score < 1000 OR sex = 1
# ORDER BY old

# если нужно отсортировать по убыванию, прописывается ключевое слово DESC:

# SELECT * FROM users
# WHERE old IN(19,32) AND score < 1000 OR sex = 1
# ORDER BY old DESC

# Если необходимо явно указать, что сортировка идёт по возрастанию возраста, то нужно прописать ASC:

# SELECT * FROM users
# WHERE old IN(19,32) AND score < 1000 OR sex = 1
# ORDER BY old ASC

# И еще один оператор для указания того, сколько записей нам надо отобразить в выборке - LIMIT:
# синтаксис следующий: LIMIT<max>[OFFSET offset] либо: LIMIT<offset,max>
# Например LIMIT 5 OFFSET 2 означает, что нужно взять 5 записей пропустив при этом первые 2.Того же результата можно
# добиться следующим синтаксисом LIMIT 2,5

# SELECT * FROM users
# WHERE old IN(19,32) AND score < 1000 OR sex = 1
# ORDER BY old ASC
# LIMIT 2,5

# создадим таблицу с данными:

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     sex INTEGER NOT NULL DEFAULT 1,
     old INTEGER,
     score INTEGER
     )""")
    cur.execute("INSERT INTO users(name,sex,old,score) VALUES('Михаил',1, 19, 1000)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Фёдор',1, 32, 200)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Николай',1, 22, 500)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Мария',2, 18, 400)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Сергей',1, 33, 2000)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Владимир',1, 43, 100)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Елена',2, 17, 500)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Юля',2, 23, 700)")

    # теперь выберем записи со счётом более 100, отсортируем их по убыванию счёта и возьмём только первые 5 из них:

    cur.execute("SELECT * FROM users WHERE score > 100 ORDER BY score DESC LIMIT 5")
    result = cur.fetchall()  # метод fetchall вызывается для получения результатов отбора sql запроса
    # print(result)
    pprint(result, indent=0, width=40)
    print()  # для отделения результатов вывода
    # [(5, 'Сергей', 1, 33, 2000),
    # (1, 'Михаил', 1, 19, 1000),
    # (8, 'Юля', 2, 23, 700),
    # (3, 'Николай', 1, 22, 500),
    # (7, 'Елена', 2, 17, 500)]

    # Либо можно в цикле перебрать все строчки из выборки. Такой вариант наиболее предпочтителен когда нужно
    # перебрать большое количество данных. Поскольку в таком случае не будет резервироваться память для большого
    # списка, а данные будут считываться (построчно) последовательно:

    cur.execute("SELECT * FROM users WHERE score > 100 ORDER BY score DESC LIMIT 5")
    for res in cur:
        print(res)
    print()
    # (5, 'Сергей', 1, 33, 2000)
    # (1, 'Михаил', 1, 19, 1000)
    # (8, 'Юля', 2, 23, 700)
    # (3, 'Николай', 1, 22, 500)
    # (7, 'Елена', 2, 17, 500)

    # Так же, если необходимо взять только какое-то определённое кол-во строк, можно использовать fetchmany:

    cur.execute("SELECT * FROM users WHERE score > 100 ORDER BY score DESC LIMIT 5")
    result = cur.fetchmany(2)  # метод fetchmany вызывается для получения конкретного кол-ва строк(в скобках)
    pprint(result, indent=0, width=40)
    # [(5, 'Сергей', 1, 33, 2000),
    # (1, 'Михаил', 1, 19, 1000)]
