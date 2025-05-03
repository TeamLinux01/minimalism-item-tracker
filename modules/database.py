import sys
import os
import sqlite3
from contextlib import closing

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "db.sqlite3"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = "db.sqlite3"
        
        try:
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

def check_database():
    with closing(conn.cursor()) as c:
        try:
            return c.execute(
                '''SELECT * FROM Item'''
            ).fetchall()
        except sqlite3.OperationalError:
            c.execute(
                '''CREATE TABLE Item (
                    pindex INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    amount INTEGER DEFAULT '1',
                    location TEXT DEFAULT '',
                    price FLOAT DEFAULT '0')'''
            )
            conn.commit()

def clearDatabase():
    with closing(conn.cursor()) as c:
        c.execute(
            '''DROP TABLE Item'''
        )
        c.execute(
                '''CREATE TABLE Item (
                    pindex INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    amount INTEGER DEFAULT '1',
                    location TEXT DEFAULT '',
                    price FLOAT DEFAULT '0')'''
            )
        conn.commit()

def load_data():
    sql = '''SELECT * FROM Item'''
    with closing(conn.cursor()) as c:
        items = c.execute(sql).fetchall()
    return items

def close():
    if conn:
        conn.close()

def add_item(item):
    sql = '''INSERT INTO Item (name, amount, location, price) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (item.name, item.amount, item.location, item.price))
        conn.commit()
