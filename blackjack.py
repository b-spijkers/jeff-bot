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
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
except Error as e:
    print(e)


def join_casino(ctx):
    userId = str(ctx.author.id)
    userName = str(ctx.author.name)
    add_user = f''' INSERT INTO user_chips VALUES ({int(userId)}, '{userName}', {0}) '''
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(add_user)
        connection.commit()

# function for getting cards needs to be added

def play_cards(ctx):
