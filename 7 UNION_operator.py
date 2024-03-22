from pprint import pprint
import sqlite3 as sq

#  Для того, что бы посмотреть как работает оператор UNION создадим 2 таблицы tab1 и tab2

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS tab1")
    cur.execute("DROP TABLE IF EXISTS tab2")
    cur.execute("""CREATE TABLE IF NOT EXISTS tab1 (
    score INTEGER PRIMARY KEY AUTOINCREMENT,
    'from' TEXT
    )""")

    cur.execute("INSERT INTO tab1 values (100, 'tab1')")
    cur.execute("INSERT INTO tab1 values (200, 'tab1')")
    cur.execute("INSERT INTO tab1 values (300, 'tab1')")

    cur.execute("""CREATE TABLE IF NOT EXISTS tab2 (
    val INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT
    )""")

    cur.execute("INSERT INTO tab2 values (200, 'tab2')")
    cur.execute("INSERT INTO tab2 values (300, 'tab2')")
    cur.execute("INSERT INTO tab2 values (400, 'tab2')")

# Выведем таблицу tab1:
    cur.execute("SELECT * FROM tab1")
    result = cur.fetchall()
    pprint(result, width=20)
    print()

    # [(100, 'tab1'),
    #  (200, 'tab1'),
    #  (300, 'tab1')]

# а так же таблицу tab2:
    cur.execute("SELECT * FROM tab2")
    result = cur.fetchall()
    pprint(result, width=20)
    print()
    # [(200, 'tab2'),
    #  (300, 'tab2'),
    #  (400, 'tab2')]


    # Применим UNION следующим образом:

    cur.execute("SELECT score, `from` FROM tab1 UNION SELECT val, type FROM tab2")
    result = cur.fetchall()
    pprint(result, width=45)
    print()

# В результате видно, что в данном случае UNION объединяет записи в порядке проверки имеющихся одинаковых записей в
# обеих таблицах в первых столбцах (200,200 и 300,300).
# [(100, 'tab1'),
#  (200, 'tab1'),
#  (200, 'tab2'),
#  (300, 'tab1'),
#  (300, 'tab2'),
#  (400, 'tab2')]
# Теперь попробуем объединить записи только по первым столбца обеих таблиц (score и val)

    cur.execute("SELECT score FROM tab1 UNION SELECT val FROM tab2")
    result = cur.fetchall()
    pprint(result, width=20)
    print()

#  В данном случае получаем лишь уникальные значения из первых столбцов обеих таблиц. В ЭТОМ И СУТЬ РАБОТЫ UNION!!!
#  Он выводит только уникальные значения данных объединяемых таблиц:
# [(100,),
#  (200,),
#  (300,),
#  (400,)]

# Можно предположить, что такой результат получился потому, что мы выбирали записи только из первых столбцов. Но нет!
# Это можно проверить изменив все записи второго столбца первой таблицы...
    cur.execute("UPDATE tab1 SET `from` = 'tab2'")
    cur.execute("SELECT * from tab1")
    result = cur.fetchall()
    pprint(result, width=20)
    print()

    cur.execute("SELECT * from tab1")
    result = cur.fetchall()
    pprint(result, width=20)
    print()
# [(200, 'tab2'),  теперь так выглядит tab1
#  (300, 'tab2'),
#  (400, 'tab2')]

# [(100, 'tab2'), а это tab2
#  (200, 'tab2'),
#  (300, 'tab2')]
# Теперь в обеих таблицах во втором столбце значения tab2. И в таком случае UNION опять объединит записи только по
# уникальным значениям первого столбца.
    cur.execute("SELECT score, `from` FROM tab1 UNION SELECT val, type FROM tab2")
    result = cur.fetchall()
    pprint(result, width=20)
    print()
# Результат:
# [(100, 'tab2'),
#  (200, 'tab2'),
#  (300, 'tab2'),
#  (400, 'tab2')]

# То есть UNION дублирует значения первого столбца только если во вторых столбцах обеих таблиц были разные значения,
# а если одинаковые, то он их объединяет в вывод только уникальных значений.

    cur.execute("UPDATE tab1 SET `from` = 'tab1'") # возвращаем первую таблицу к первоначальному виду


# Так же можно объединять и следующим образом... Укажем явно значения во вторых столбцах таблиц. Например,
# table 1 и table 2. При этом в первой таблице укажем синоним as tbl, чтоб СУБД знала как назвать этот второй
# столбец
    cur.execute("SELECT score, 'table 1' as tbl FROM tab1 UNION SELECT val, 'table 2' FROM tab2")
# получим:
    result = cur.fetchall()
    pprint(result)
    print()

# [(100, 'table 1'),
#  (200, 'table 1'),
#  (200, 'table 2'),
#  (300, 'table 1'),
#  (300, 'table 2'),
#  (400, 'table 2')]

# Ну и во всём этом можно так же сделать сортировку. Например, так: по полю score

    cur.execute("SELECT score, 'table 1' as tbl FROM tab1 UNION SELECT val, 'table 2' FROM tab2 ORDER BY score DESC")
    result = cur.fetchall()
    pprint(result,width=20)
    print()
# [(400, 'table 2'),
#  (300, 'table 1'),
#  (300, 'table 2'),
#  (200, 'table 1'),
#  (200, 'table 2'),
#  (100, 'table 1')]

# А так же можно поставить фильтр IN (300, 400) и поставить лимит вывода записей LIMIT 3
    cur.execute("""SELECT score, 'table 1' as tbl FROM tab1 WHERE score IN (300, 400) 
    UNION SELECT val, 'table 2' FROM tab2 
    ORDER BY score DESC
    LIMIT 3""")
    result = cur.fetchall()
    pprint(result,width=20)
    print()

# [(400, 'table 2'),
#  (300, 'table 1'),
#  (300, 'table 2')]

