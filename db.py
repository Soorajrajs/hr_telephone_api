import sqlite3

conn = sqlite3.connect("telephone.sqlite")

cursor=conn.cursor()

sql_query="""CREATE TABLE telephone (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                number INTEGER NOT NULL UNIQUE,
                company TEXT NOT NULL ) """

cursor.execute(sql_query)