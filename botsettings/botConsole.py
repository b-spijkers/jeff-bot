import time


def log_command(ctx):
    """

    :param ctx: context of discord bot
    :return: prints Command name to console with User, Guild, GuildID and time as additional info
    """
    print(
        'Command: ' + ctx.invoked_with + ' \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime(
            "%Y-%m-%d %H:%M \n"
        )
    )
