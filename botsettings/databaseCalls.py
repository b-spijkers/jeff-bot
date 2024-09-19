import os

from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_DATABASE = os.getenv("DATABASE")


try:
    connection = connect(
        host=DB_HOST,
        user='root',
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
except Error as e:
    print(e)


def update_db(query):
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(query)
        connection.commit()


def insert_db(query):
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(query)
        connection.commit()


def select_one_db(query):
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(query)
        row = cursor.fetchone()
        if row is None:
            row = ['bleh']
        return row[0]


def delete_db(query):
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(query)
        connection.commit()
