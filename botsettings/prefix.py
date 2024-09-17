from botsettings import botConsole
from botsettings.databaseCalls import insert_db, update_db, select_one_db, delete_db


def get_prefix(bot, message):  # first we define get_prefix
    current_guild = str(message.guild.id)
    select_prefix = f""" SELECT guild_prefix FROM prefixes WHERE guild_id = {current_guild} """
    guild_prefix = select_one_db(select_prefix)

    return guild_prefix


def add_guild(guild):
    current_guild = str(guild.id)
    current_guild_name = str(guild.name)

    add_to_db = f""" INSERT INTO prefixes VALUES ('{current_guild}', '//') """
    insert_db(add_to_db)


def remove_guild(message):
    current_guild = str(message.guild.id)
    delete_guild = f""" DELETE FROM prefixes WHERE guild_id = '{current_guild}' """
    delete_db(delete_guild)


async def new_prefix(ctx, prefix):
    if prefix is None:
        return await ctx.send(f'Please set a new prefix by typing the new prefix after the command')
    else:
        botConsole.log_command(ctx)

        current_guild = str(ctx.guild.id)
        update_prefix = f""" UPDATE prefixes SET guild_prefix = '{prefix}' WHERE guild_id = {current_guild} """

        update_db(update_prefix)

        return await ctx.send(f'Prefix changed to: {prefix}')  # confirms the prefix it's been changed to
