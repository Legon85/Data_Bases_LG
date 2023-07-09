from pprint import pprint
import sqlite3 as sq

# Для рассмотрения вопроса объединения данных из 2-х и более разных таблиц для формирования сводного отчёта,
# создадим ещё одну таблицу users:

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     name TEXT,
     sex INTEGER,
     old INTEGER,
     score INTEGER
     )""")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Михаил',1, 22, 1000)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Яна',2, 24, 830)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Фёдор',1, 32, 764)")

    cur.execute("DROP TABLE IF EXISTS games")
    cur.execute("""CREATE TABLE IF NOT EXISTS games (
     user_id INTEGER,
     score INTEGER,
     time INTEGER
     )""")
    cur.execute("INSERT INTO games(user_id, score, time) VALUES(1, 200, 100000)")
    cur.execute("INSERT INTO games (user_id, score, time) VALUES(1, 300, 110010)")
    cur.execute("INSERT INTO games (user_id, score, time) VALUES(2, 500, 100010)")
    cur.execute("INSERT INTO games (user_id, score, time) VALUES(1, 400, 201034)")
    cur.execute("INSERT INTO games (user_id, score, time) VALUES(3, 100, 200010)")
    cur.execute("INSERT INTO games (user_id, score, time) VALUES(2, 600, 210000)")
    cur.execute("INSERT INTO games (user_id, score, time) VALUES(2, 300, 210010)")

    # Теперь у нас есть 2 таблицы games и users и мы можем по 2-м ключам из этих разных таблиц взять и получить
    # данные, связанные по этим ключам, с помощью оператора JOIN по синтаксису: JOIN<таблица>ON<условие связывания>
    # Ключом из таблицы games будет user_id (он называется внешним ключом), а ключом из таблицы users будет
    # row_id (он называется первичным ключом).
    # Предположим нам надо получить данные name и sex из таблицы users в объединении с данными score,
    # но уже из таблицы games!
    # И это можно сделать по следующему синтаксису:
    # SELECT           команда выборки
    # name,sex,games.score  (games.score как раз означает, что score мы будем брать из таблицы games а не из users)
    # FROM games       тут указывается какая таблица будет первичной(главной)
    # JOIN users       здесь мы говорим какую таблицу будем связывать таблицей games
    # ON games.user_id = users.rowid       и здесь уже идёт условие связывания (т.е. у нас поле user_id из таблицы
    # games должно быть равно полю rowid из таблицы suers

    cur.execute("SELECT name, sex, games.score FROM games JOIN users ON games.user_id = users.rowid ")
    result = cur.fetchall()
    pprint(result, width=45)
    print()
    # получаем:
    # [('Михаил', 1, 200),
    #  ('Михаил', 1, 300),
    #  ('Яна', 2, 500),
    #  ('Михаил', 1, 400),
    #  ('Фёдор', 1, 100),
    #  ('Яна', 2, 600),
    #  ('Яна', 2, 300)]

    # В вышеописанном мы используем JOIN когда есть полное соответствие связываемых данных в таблицах (user_id в
    # таблице games и rowid в таблице games). И в действительности использование такого JOIN есть аналог так
    # называемого INNER JOIN. То есть соединение записей из двух таблиц если соответствия в них были найдены.
    # Если же, например, из таблицы users удалить запись с rowid = 3 (а именно 'Фёдор',1, 32, 764),
    # то при использовании JOIN(INNER JOIN) в сводной таблице будет отсутствовать запись ('Фёдор', 1, 100):

    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     name TEXT,
     sex INTEGER,
     old INTEGER,
     score INTEGER
     )""")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Михаил',1, 22, 1000)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Яна',2, 24, 830)")

    cur.execute("SELECT name, sex, games.score FROM games JOIN users ON games.user_id = users.rowid ")
    result = cur.fetchall()
    pprint(result, width=45)
    print()
    # [('Михаил', 1, 200),
    #  ('Михаил', 1, 300),
    #  ('Яна', 2, 500),
    #  ('Михаил', 1, 400),
    #  ('Яна', 2, 600),
    # ('Яна', 2, 300)]  в выводе видно, что отсутствует ('Фёдор', 1, 100)

    # Но иногда важно иметь все записи из главной таблицы games, а дополнительные сведения из второй таблицы
    # добавлять если они там есть. Для такого вывода данных используется модификация LEFT JOIN. И тогда

    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     name TEXT,
     sex INTEGER,
     old INTEGER,
     score INTEGER
     )""")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Михаил',1, 22, 1000)")
    cur.execute("INSERT INTO users (name,sex,old,score) VALUES('Яна',2, 24, 830)")

    cur.execute("SELECT name, sex, games.score FROM games LEFT JOIN users ON games.user_id = users.rowid ")
    result = cur.fetchall()
    pprint(result, width=45)
    print()
    # получаем:
    # [('Михаил', 1, 200),
    #  ('Михаил', 1, 300),
    #  ('Яна', 2, 500),
    #  ('Михаил', 1, 400),
    #  (None, None, 100),  то есть тут как бы была сыграна игра неизвестным пользователем который набрал 100 очков
    #  ('Яна', 2, 600),
    #  ('Яна', 2, 300)]
