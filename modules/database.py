import sys
import os
import sqlite3
from contextlib import closing

conn = None

def connect():
    '''Opens the database connection if it is not opened'''
    global conn
    if not conn:
        if sys.platform == "win32":     # If OS is Windows
            DB_FILE = "db.sqlite3"      # Use filename "db.sqlite3"
        else:
            HOME = os.environ["HOME"]   # If OS is MacOS, Linux or Unix
            DB_FILE = "db.sqlite3"      # Use filename "db.sqlite3"
        
        try:
            conn = sqlite3.connect(DB_FILE) # Creates the database connection to file
            conn.row_factory = sqlite3.Row  # Allows rows to use names instead of index numbers
        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

def check_database():
    '''Checks if "Item" table exists, creates it if it does not
       Also returns all items in the database'''
    with closing(conn.cursor()) as c:
        try:
            return c.execute(               # Tries to return all items in the database
                '''SELECT * FROM Item'''
            ).fetchall()
        except sqlite3.OperationalError:
            c.execute(                      # Creates the "Item" table if it fails to find any data in the "Item" table
                '''CREATE TABLE Item (
                    pindex INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    amount INTEGER DEFAULT '1',
                    location TEXT DEFAULT '',
                    price FLOAT DEFAULT '0')'''
            )
            conn.commit()

def clearDatabase():
    '''Destroys the "Item" table and recreates it'''
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
