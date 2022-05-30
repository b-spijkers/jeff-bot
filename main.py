import discord
import commands

from discord.utils import find

client = discord.Client()


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Fuck')


@client.event
async def on_ready():
    print('{0.user}'.format(client) + ' is online and ready')


@client.event
async def on_message(message):
    mentions = message.mentions

    if message.author == client.user:
        return

    if message.content.startswith(f'#beadick'):
        if message.mentions:
            insult = commands.get_insult()
            await message.channel.send('<@' + str(message.mentions[0].id) + '> ' + insult)
        else:
            insult = commands.get_insult()
            await message.channel.send(message.author.mention + ' ' + insult)

    if message.content.startswith(f'#help'):
        await message.channel.send(
            f'Commands are: `#beadick`, `#because`, `#give`, `#cool`, `#fasc` and `#yoda` for now.')

    if message.content.startswith(f'#because'):
        if message.mentions:
            because = commands.throw_because(str(message.author.mention))
            await message.channel.send('<@' + str(message.mentions[0].id) + '> ' + because)
        else:
            because = commands.throw_because(str(message.author.mention))
            await message.channel.send(because)

    if message.content.startswith(f'#give'):
        if message.mentions:
            give = commands.throw_give(str(message.author.mention))
            await message.channel.send('<@' + str(message.mentions[0].id) + '> ' + give)
        else:
            give = commands.throw_give(str(message.author.mention))
            await message.channel.send(give)

    if message.content.startswith(f'#cool'):
        if message.mentions:
            cool = commands.throw_cool(str(message.author.mention))
            await message.channel.send('<@' + str(message.mentions[0].id) + '> ' + cool)
        else:
            cool = commands.throw_cool(str(message.author.mention))
            await message.channel.send(cool)

    if message.content.startswith(f'#fasc'):
        if message.mentions:
            fasc = commands.throw_fascinating(str(message.author.mention))
            await message.channel.send('<@' + str(message.mentions[0].id) + '> ' + fasc)
        else:
            fasc = commands.throw_fascinating(str(message.author.mention))
            await message.channel.send(fasc)

    if message.content.startswith(f'#yoda'):
        if message.mentions:
            mentioned = '<@' + str(message.mentions[0].id) + '>'
            yoda = commands.throw_yoda(mentioned)
            await message.channel.send(yoda)
        else:
            error = 'Good job, idiot. Command is `#yoda <@mention>`'
            await message.channel.send(error)


client.run('OTgwNzk4MzAxNDcxNDA0MDYy.Gn_FSl.B-AzhCNYmEmBub-92zef29YQYri4jnwwHwZgJk')
