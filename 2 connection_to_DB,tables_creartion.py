# для начала работы нужно подключить модуль далее:
import sqlite3 as sq  # для удобства зададим синоним sq


# Далее мы вызываем метод connect() который устанавливает связь с некой базой данных. Причём этот файл
# с которым устанавливается связь должен быть в том же каталоге. Если его нет, то он создастся
# автоматически

con = sq.connect("saper.db")

# далее для непосредственного взаимодействия с БД нужно использовать объект cursor(). Метод cursor
# возвращает экземпляр класса Cursor и уже через него осуществляем непосредственную работу.
cur = con.cursor() # Cursor
# В самом простом случае можно вызвать метод execute() которому передаётся sql-запрос для работы с БД
cur.execute(""" """)

# после работы с БД её надо обязательно закрыть вызовом метода close у объекта connection
# на который ссылается переменная con:
con.close()

# способ открытия для работы БД описанный выше не самый лучший вариант т.к. в случае ошибок не сработает
# метод close и база не закроется. А делать это лучше через контекстный менеджер:

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute(""" """)

# Для создания таблицы нужно передать методу execute определённые аргументы:
# запрос типа CREATE TABLE (пишутся большими буквами) users создаст таблицу с названием users.
# И далее в скобках перечисляем
# все поля таблицы (пишутся маленькими буквами) с типами вводимых данных)

# with sq.connect("saper.db") as con:
#     cur = con.cursor()
#     cur.execute("""CREATE TABLE users (
#      name TEXT,
#      sex INTEGER,
#      old INTEGER,
#      score INTEGER
#      )""")

# Но если попытаться ещё раз запустить эту программу, то мы получим ошибку, говорящую о том что
# мы пытаемся создать таблицу, но она уже существует. Поэтому лучше подредактировать sql-запрос
# CREATE TABLE IF NOT EXIST чтобы таблица создавалась только если её ещё не было создано

with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     name TEXT, 
     sex INTEGER,
     old INTEGER,
     score INTEGER
     )""")

# Для удаления таблицы используется sql-запрос (команда) "DROP TABLE <название таблицы>":
with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE  users")

# При создании полей так же можно указывать так называемые ограничители. Например, если нужно, что бы
# поле "name" никогда не было пустым можно прописать ограничитель "NOT NULL". А если нужно,
# что бы, в случае если в поле "sex" не введут данные, оно по умолчанию ставило бы значение "1",
# то нужно прописать ограничитель "DEFAULT 1"
# так же можно прописать одновременно "NOT NULL DEFAULT 1" например в поле sex. Тогда будут соблюдены
# оба ограничителя

# если вновь создадим таблицу с ограничителями, то увидим их во вкладке "структура БД" - поле "схема" и
# в соответствующих полях, во-первых, не будет NULL, во-вторых, там где не были проставлены значения будут
# стоять 1-цы
with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     name TEXT NOT NULL, 
     sex INTEGER DEFAULT 1,
     old INTEGER,
     score INTEGER
     )""")

# Так же в любой таблице можно создавать поля такого типа: user_id INTEGER PRIMARY KEY. Где PRIMARY KEY
# означает что поле будет являться главным ключом, а значит должно содержать уникальные значения.
# Создадим такую таблицу, удалив сначала старую с добавлением "IF EXIST" для того, чтоб в случае
# отсутствия таблиц при удалении не выводились ошибки типа: no such tables:
with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS users") # используем IF EXIST

# создаём новую
with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     user_id INTEGER PRIMARY KEY,
     name TEXT NOT NULL, 
     sex INTEGER DEFAULT 1,
     old INTEGER,
     score INTEGER
     )""")

# Теперь таблица имеет поле user_id и, при заполнении её данными, это поле автоматически заполняется
# уникальными номерами по порядку. Правда для автоматического увеличения этого значения на единицу,
# несмотря на то, что вроде бы, поле и так автоматически увеличивается на 1 при добавлении записей,
# ещё предусмотрен ограничитель AUTOINCREMENT. При этом автоматически создаётся внутренняя таблица
# sqlite_sequence необходимая для реализации AUTOINCREMENT.
with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("DROP TABLE users") # используем IF EXIST

# создаём новую
with sq.connect("saper.db") as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     sex INTEGER DEFAULT 1,
     old INTEGER,
     score INTEGER
     )""")