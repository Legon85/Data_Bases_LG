import sqlite3 as sq

with sq.connect("saper.db") as con:
    cur = con. cursor()
    cur.execute("DROP TABLE IF EXISTS tab1")
    cur.execute("""CREATE TABLE IF NOT EXISTS tab1 (
    score INTEGER,
    'from' TEXT
    )""")

    cur.execute("INSERT INTO tab1(score) VALUES(100)")

