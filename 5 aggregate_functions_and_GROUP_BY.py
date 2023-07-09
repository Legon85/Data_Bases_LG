from pprint import pprint
import sqlite3 as sq

# Рассмотрим агрегирующие функции в языке sql и возможность группировки записей по определённому полю
# Все эти операции доступны по команде SELECT

# Рассмотрим пример подсчёта числа записей в таблице games, которые были сыграны первым игроком
# создадим таблицу:

with sq.connect("saper.db") as con:
    cur = con.cursor()
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

    # Выведем сначала все записи связанные с первым игроком (user_id = 1)
    cur.execute("SELECT user_id FROM games WHERE user_id = 1")
    result = cur.fetchall()
    pprint(result, width=15)
    print()

    # А чтобы вывести не просто эти записи, а их количество, как раз и используются агрегирующие функции
    # в данном случае мы используем функцию count и вот её синтаксис:

    cur.execute("SELECT count(user_id) FROM games WHERE user_id = 1")
    result = cur.fetchall()
    print(result)  # получаем значение [(3,)], что верно (таких записей в таблице - 3)
    print()

    # Вообще в данном случае в скобках функции count можно прописать, например, score или вообще ничего не
    # прописывать, поскольку всё равно вывод будет тот же ([(3,)]) потому что это определено в условии
    # WHERE user_id = 1

    # В программе DB Browser в шапке с названиями полей при выводе таблицы с результатом вышеописанного запроса
    # с функцией count будет название типа count() либо count(user_id) либо count(score), что не очень удобно.
    # Поэтому для удобства можно задавать синонимы посредством синтаксиса  as + <синоним>:
    # "SELECT count(user_id) as count FROM games WHERE user_id = 1"

    # Помимо ф-ции count существуют следующие ф-ции:
    # sum() - подсчёт суммы указанного поля по всем записям выборки
    # avr() - вычисление среднего арифметического указанного поля
    # min() - нахождение мин значения для указанного поля
    # max() - нахождение макс значения для указанного поля

    # Рассмотрим как можно подсчитать кол-во уникальных игроков в таблице. Для этого нужно прописать ключевое
    # слово DISTINCT и убрать условие выборки WHERE :
    cur.execute("SELECT count(DISTINCT user_id) FROM games")
    result = cur.fetchall()
    print(result)  # получаем [(3,)], что верно т.к. у нас 3 уникальных игрока
    print()

    # Теперь посчитаем суммарное количество очков, которое набрал 1-ый игрок во всех играх. Для этого используем
    # вместо count   sum  и фильтр WHERE user_id = 1:
    cur.execute("SELECT sum(score) as scores FROM games WHERE user_id = 1")
    result = cur.fetchall()
    print(result)  # получаем  [(900,)]
    print()

    # то же самое можно сделать и для функций max min:
    cur.execute("SELECT max(score) as scores FROM games WHERE user_id = 1")
    result = cur.fetchall()
    print(result)  # [(400,)]
    print()

    cur.execute("SELECT min(score) as scores FROM games WHERE user_id = 1")
    result = cur.fetchall()
    print(result)  # [(200,)]
    print()

    # Далее о группировке записей GROUP BY:
    # Предположим нужно посчитать максимальное количество очков за игры для каждого игрока, а не для одного или
    # всех сразу.
    # Агрегирующие функции, рассмотренные выше, работают только в рамках определённой группы. А сама группа
    # определяется с помощью оператора GROUP BY. Синтаксис: GROUP BY<имя поля>. В нашем случае именем поля будет
    # как раз номер игрока (то есть в общем случае идентификатор группы для которой будет выполняться функция
    # агрегирования):
    cur.execute("SELECT user_id, sum(score) as sum FROM games GROUP BY user_id")
    result = cur.fetchall()
    pprint(result, width=15)
    print()
    print()
    # получаем:
    # [(1, 900),
    #  (2, 1400),
    #  (3, 100)]

    # Сделаем сортировку по убыванию данных полученных выше. Для этого добавим ORDER BY sum DESC:
    cur.execute("SELECT user_id, sum(score) as sum FROM games GROUP BY user_id ORDER BY sum DESC")
    result = cur.fetchall()
    pprint(result, width=15)
    print()
    #  получаем:
    #  [(2, 1400),
    #  (1, 900),
    #  (3, 100)]

    #  Добавим фильтр, который будет суммировать только счета более 300 очков
    cur.execute("SELECT user_id, sum(score) as sum FROM games WHERE score > 300 GROUP BY user_id ORDER BY sum "
                "DESC")
    result = cur.fetchall()
    pprint(result, width=15)
    print()
    # получаем:
    # [(2, 1100),
    #  (1, 400)]

    # Ну и если нужно сделать ограничение по числу выводимых записей, то в последнюю очередь ставится оператор
    # LIMIT:
    cur.execute("SELECT user_id, sum(score) as sum FROM games WHERE score > 300 GROUP BY user_id ORDER BY sum "
                "DESC LIMIT 1")
    result = cur.fetchall()
    pprint(result, width=15) # получаем [(2, 1100)]  одну запись
    print()