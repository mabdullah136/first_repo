from flask import Flask
from markupsafe import escape
import sqlite3

app = Flask(__name__)


def create_tables():
    conn = sqlite3.connect('practice')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            email TEXT,
            address TEXT,
            total_orders INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            price REAL,
            date_of_purchase TEXT,
            total_paid REAL,
            order_status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer (id),
            FOREIGN KEY (product_id) REFERENCES product (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_price REAL,
            product_color TEXT,
            product_image TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_tables()




