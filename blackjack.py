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


def check_entry(ctx):
    userId = str(ctx.author.id)
    find_user = f''' SELECT user_id FROM user_chips WHERE user_id = {userId} '''
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(find_user)
        user_id = cursor.fetchone()[0]


def join_casino(ctx):
    userId = str(ctx.author.id)
    userName = str(ctx.author.name)
    add_user = f''' INSERT INTO user_chips VALUES ({int(userId)}, '{userName}', {0}) '''
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(add_user)
        connection.commit()


# function for getting cards needs to be added, and coinflips


def coinflip(ctx, side, amount):
    userId = str(ctx.author.id)
    if side == 'h':
        side = 'heads'
    if side == 't':
        side = 'tails'
    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_id = {userId}'''
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(get_chips)
        amount_chips = cursor.fetchone()
    amount_chips = amount_chips[0]
    if amount == 'a':
        amount = amount_chips
    elif amount == 'h':
        amount = amount_chips / 2
    if int(amount) > 0:
        amount_chips = amount_chips + int(amount)
        update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_id = {userId} """
        with connection.cursor() as cursor:
            connection.reconnect()
            cursor.execute(update_chips)
            connection.commit()
        return 'Wow! it was ' + side + "! You're amazing 🎉. You now have: " + str(amount_chips) + ' chips'
    else:
        return "Nice, you're broke 🤣"


