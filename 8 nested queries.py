from pprint import pprint
import sqlite3 as sq

#  Для того, что бы посмотреть как работают вложенные запросы создадим 2 таблицы students и marks

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sex INTEGER,
    old INTEGER
    )""")

    cur.execute("INSERT INTO students (name,sex,old) VALUES('Коля',1, 17)")
    cur.execute("INSERT INTO students (name,sex,old) VALUES('Маша',2, 18)")
    cur.execute("INSERT INTO students (name,sex,old) VALUES('Вася',1, 19)")
    cur.execute("INSERT INTO students (name,sex,old) VALUES('Даша',2, 17)")

    cur.execute("SELECT * FROM students")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    # [(1, 'Коля', 1, 17),
    #  (2, 'Маша', 2, 18),
    #  (3, 'Вася', 1, 19),
    #  (4, 'Даша', 2, 17)]

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS marks")
    cur.execute("""CREATE TABLE IF NOT EXISTS marks (
    id INTEGER ,
    subject TEXT,
    mark INTEGER
    )""")

    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(1,'Си', 4)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(1,'Физика', 3)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(1,'Вышка', 5)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(1,'Физра', 5)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(2,'Си', 3)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(2,'Вышка', 4)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(2,'Химия', 3)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(3,'Си', 4)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(3,'Черчение', 3)")
    cur.execute("INSERT INTO marks (id,subject,mark) VALUES(3,'Физика', 5)")

    cur.execute("SELECT * FROM marks")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    # [(1, 'Си', 4),
    #  (1, 'Физика', 3),
    #  (1, 'Вышка', 5),
    #  (1, 'Физра', 5),
    #  (2, 'Си', 3),
    #  (2, 'Вышка', 4),
    #  (2, 'Химия', 3),
    #  (3, 'Си', 4),
    #  (3, 'Черчение', 3),
    #  (3, 'Физика', 5)]

    #  Задача: выбрать всех студентов у которых оценка по языку Си выше чем оценка по этому же языку Си у Маши
    #  По идее нужно реализовать 2 запроса. При первом мы определяем какую оценку получила Маша по языку Си и далее
    #  составляем запрос для всех студентов у которых оценка по этому языку выше чем у Маши

    #  Первый запрос:

    cur.execute("SELECT mark FROM marks WHERE id = 2 AND subject LIKE 'Си'")
    result = cur.fetchall()
    pprint(result, indent=0, width=40)
    print("--" * 40)

    #  Output: [(3,)]

    # второй запрос:

    cur.execute("SELECT name, subject, mark FROM marks JOIN students ON students.rowid = marks.id WHERE mark > 3 AND "
                "subject LIKE 'Си'")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # [('Коля', 'Си', 4),
    #  ('Вася', 'Си', 4)]

    #  Так вот в sql можно вышеописанное объединить в один запрос с помощью вложенных запросов. В данном случае надо
    #  взять и скопировать первый запрос и вставить его в скобках во второй запрос вместо 3-ки. Тем самым как бы заменив
    #  3-ку уже сделанным запросом, который и выводит 3-ку:

    cur.execute("SELECT name, subject, mark FROM marks JOIN students ON students.rowid = marks.id WHERE mark > "
                "(SELECT mark FROM marks WHERE id = 2 AND subject LIKE 'Си') "
                "AND subject LIKE 'Си'")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # [('Коля', 'Си', 4),
    #  ('Вася', 'Си', 4)]

    #  Если в запросе убрать условие AND subject LIKE 'Си', то, несмотря на это результат будет тем же, потому что при
    #  выполнении вложенного запроса будет выбрана первая запись относящаяся к условию WHERE id = 2:

    cur.execute("SELECT name, subject, mark FROM marks JOIN students ON students.rowid = marks.id WHERE mark > "
                "(SELECT mark FROM marks WHERE id = 2) "
                "AND subject LIKE 'Си'")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # [('Коля', 'Си', 4),
    #  ('Вася', 'Си', 4)]

    #  Если же вложенный запрос вернёт Null (то-есть ни одной записи), то внешний тоже не вернёт ни одной записи:

    cur.execute("SELECT name, subject, mark FROM marks JOIN students ON students.rowid = marks.id WHERE mark > "
                "(SELECT mark FROM marks WHERE id = 4) "  # заменили 2 на 4 для примера невозвращения ничего
                "AND subject LIKE 'Си'")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # []

    #  Так же можно использовать агрегирующие ф-ции во вложенных запросах. Выберем для Маши среднее арифметическое наших
    #  оценок avg(mark) FROM marks. Правда получим тот же вывод потому что средняя оценка 3 с небольшим:

    cur.execute("SELECT name, subject, mark FROM marks JOIN students ON students.rowid = marks.id WHERE mark > "
                "(SELECT avg(mark) FROM marks WHERE id = 2) "  # заменили 2 на 4 для примера невозвращения ничего
                "AND subject LIKE 'Си'")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # [('Коля', 'Си', 4),
    # ('Вася', 'Си', 4)]

#  Так же влож. запросы можно использовать и в команде INSERT. Для примера создадим таблицу female и добавим туда
#  всех студентов женского пола

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS female")
    cur.execute("""CREATE TABLE IF NOT EXISTS female (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sex INTEGER,
    old INTEGER
    )""")

    #  Далее создадим запрос реализующий нужный нам функционал
    cur.execute("INSERT INTO female SELECT * FROM students WHERE sex = 2")
    #  Во вложенном запросе производится выборка из таблицы students всех студентов женского пола
    cur.execute("SELECT * FROM female")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # [(2, 'Маша', 2, 18),
    # (4, 'Даша', 2, 17)]

    #  Но у такого запроса есть недостаток: если его выполнить 2 раза будет ошибка потому что у поля id в таблице female
    #  должны быть уникальные значения и добавляться автоматически, а при повторной вставке будут вставляться те же
    #  значения id:

    # cur.execute("INSERT INTO female SELECT * FROM students WHERE sex = 2")
    # --> sqlite3.IntegrityError: UNIQUE constraint failed: female.id

    #  Поэтому лучше конкретно указать какие поля записывать и первому полю (id) прописать Null:
    cur.execute("INSERT INTO female SELECT NULL, name, sex, old FROM students WHERE sex = 2")

    cur.execute("SELECT * FROM female")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    #     [(2, 'Маша', 2, 18),
    #       (4, 'Даша', 2, 17),
    #       (5, 'Маша', 2, 18),
    #       (6, 'Даша', 2, 17)

    #  Для команды update так же можно использовать влож. запросы. Допустим нужно обнулить оценки в таблице marks,
    #  которые меньше или равны минимальной оценке студента с id = 1. Можно записать такой запрос в следующем виде

    cur.execute("UPDATE marks SET mark = 0 WHERE mark <= (SELECT min(mark) FROM marks WHERE id= 1)")

    cur.execute("SELECT * FROM marks")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

    # [(1, 'Си', 4),
    #  (1, 'Физика', 0),
    #  (1, 'Вышка', 5),
    #  (1, 'Физра', 5),
    #  (2, 'Си', 0),
    #  (2, 'Вышка', 4),
    #  (2, 'Химия', 0),
    #  (3, 'Си', 4),
    #  (3, 'Черчение', 0),
    #  (3, 'Физика', 5)]

#  Так же можно использовать вложенный запросы в команде DELETE. Допустим нужно удалить из таб. students всех
#  студентов возраст которых меньше чем у Маши:

    cur.execute("DELETE FROM students WHERE old < (SELECT old FROM students WHERE id = 2)")

    cur.execute("SELECT * FROM students")
    result = cur.fetchall()
    pprint(result, indent=0, width=20)
    print("--" * 40)

# [(2, 'Маша', 2, 18),
# (3, 'Вася', 1, 19)]



