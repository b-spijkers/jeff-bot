import os

from dotenv import load_dotenv
from mysql.connector import connect, Error
from botsettings import botConsole

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
    print('Connected to database')
except Error as e:
    print(e)


def get_prefix(bot, message):  # first we define get_prefix
    current_guild = str(message.guild.id)
    select_prefix = f""" SELECT guild_prefix FROM prefixes WHERE guild_id = {current_guild} """
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(select_prefix)
        guild_prefix = cursor.fetchall()[0]
    return guild_prefix


def add_guild(message):
    current_guild = str(message.guild.id)
    current_guild_name = str(message.guild.name)
    add_to_db = f""" INSERT INTO prefixes VALUES ({current_guild}, {current_guild_name}, '//') """
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(add_to_db)
        connection.commit()


def remove_guild(message):
    current_guild = str(message.guild.id)
    delete_guild = f""" DELETE FROM prefixes WHERE guild_id = {current_guild} """
    with connection.cursor() as cursor:
        connection.reconnect()
        cursor.execute(delete_guild)
        connection.commit()


async def new_prefix(ctx, prefix):
    if prefix is None:
        return await ctx.send(f'Please set a new prefix by typing the new prefix after the command')
    else:
        botConsole.log_command(ctx)

        current_guild = str(ctx.guild.id)
        update_prefix = f""" UPDATE prefixes SET guild_prefix = '{prefix}' WHERE guild_id = {current_guild} """

        with connection.cursor() as cursor:
            connection.reconnect()
            cursor.execute(update_prefix)
            connection.commit()

        return await ctx.send(f'Prefix changed to: {prefix}')  # confirms the prefix it's been changed to
