import random
import requests
import json
import discord


# Just some commands I find funny or are just generally pretty fun


async def dad(ctx):
    response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    joke = json_data['joke']

    msg = discord.Embed(
        title="Hi, I'm dad",
        description=joke,
        color=0xFF5733,
    )
    return await ctx.channel.send(embed=msg)


async def dumbledore(ctx):
    response = requests.get('https://foaas.com/dumbledore/' + str(ctx.author.mention) + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    msg = json_data['message']
    await ctx.channel.send(msg)


def yoda(name):
    yoda = 'Fuck off, you must, ' + name
    return yoda


def insult():
    response = requests.get('https://insult.mattbas.org/api/insult')
    insult = response.text
    return insult


async def kill_none(ctx):
    msg = discord.Embed(
        title='Uh oh! Someone is a poopie head!',
        description='Must @mention someone you egg!',
        color=discord.Color.red()
    )
    await ctx.channel.send(embed=msg)


async def kill_everyone(bot, ctx):
    msg = discord.Embed(
        description="Jeff is done with this planet",
        color=discord.Color.blurple()
    )
    msg.set_footer(
        text="Requested by: {}".format(
            ctx.author.display_name
        ) + ". Jeff has always wanted to do this"
    )
    msg.set_image(url='https://c.tenor.com/RjAxaS7VppAAAAAC/deathstar.gif')
    msg.set_author(
        name=bot.user.display_name,
        icon_url=bot.user.avatar_url
    )
    await ctx.channel.send(embed=msg)


async def kill(bot, ctx):
    author_of_msg = str(ctx.author.mention)
    victim = '<@!' + str(ctx.message.mentions[0].id) + '>'

    kill_gifs = [
        'https://media.giphy.com/media/RLi2oeVZiVkE8/giphy.gif',
        'https://media.giphy.com/media/uAH7abSiUAlPO/giphy.gif',
        'https://c.tenor.com/YNK5CjT9dw8AAAAC/kill-wasted.gif',
        'https://c.tenor.com/mZ1h2IELTmoAAAAC/wasted-shovel.gif',
        'https://c.tenor.com/6BEtB9KcY2YAAAAC/funny-kid.gif',
        'https://c.tenor.com/t25gIlKm8UEAAAAC/murderer-pillow.gif',
        'https://c.tenor.com/9jf-DDWOCI4AAAAC/runover-kid.gif'
    ]

    suicide_gifs = [
        'https://media.giphy.com/media/AHMHuF12pW4b6/giphy.gif',
        'https://media.giphy.com/media/FWuAGe5KQQVNu/giphy.gif',
        'https://c.tenor.com/tDHcVAwpsbEAAAAC/wasted-funny.gif',
        'https://c.tenor.com/HMc73AnstjEAAAAC/wasted-gta-v.gif',
        'https://c.tenor.com/iEjB32ZQlesAAAAC/epic-meme.gif',
        'https://media3.giphy.com/media/w29hHnsoaqsy4/giphy.gif?cid=790b7611b892a8e0f1f62a050c49599ace21d60598f91bd2&rid=giphy.gif&ct=g',
        'https://c.tenor.com/2gIn6DLSTOcAAAAd/general-grievous-star-wars.gif'
    ]

    if '!' not in author_of_msg:
        author = author_of_msg[:2] + '!' + author_of_msg[2:]
        author_of_msg = author

    if author_of_msg == victim:
        gif = random.choice(suicide_gifs)
    else:
        gif = random.choice(kill_gifs)

    if bot.user.mentioned_in(ctx.message):
        gif = 'https://c.tenor.com/N1eC5_O9KiAAAAAd/justketh-goose-attack.gif'
        msg = discord.Embed(
            description='Nice try, bitch!',
            color=discord.Color.red()
        )
        msg.set_author(
            name=bot.user.display_name,
            icon_url=bot.user.avatar_url
        )
        msg.set_image(url=gif)
        await ctx.channel.send(embed=msg)
    elif author_of_msg == victim:
        suicide_messages = [
            ' robloxed themselves',
            ' committed neck rope',
            ' game overed themselves',
            ' wasted themselves'
        ]

        msg = discord.Embed(
            description=str(ctx.author.mention) + random.choice(suicide_messages),
            color=discord.Color.red()
        )
        msg.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        )
        msg.set_image(url=gif)
        await ctx.channel.send(embed=msg)
    else:
        killed_messages = [
            ' brutalized ',
            ' murdered ',
            ' rekt ',
            ' game overed ',
            ' fucked up ',
            ' terminated ',
            ' killed ',
            ' wasted ',
            " KO'd "
        ]

        msg = discord.Embed(
            description=str(ctx.author.mention) + random.choice(killed_messages) + '<@' + str(
                ctx.message.mentions[0].id
            ) + '>',
            color=discord.Color.blue()
        )
        msg.set_image(url=gif)
        await ctx.channel.send(embed=msg)


# Nicht rijder zooi, born 2 be alive is van The Village People, iedereen weet dat. Wat is een Patrick Hernandez? Idk
def nicht():
    return 'https://www.youtube.com/watch?v=Pie6izHuaMU'


def b2ba():
    return 'https://www.youtube.com/watch?v=YajODJwJhwk'


async def kingbas(ctx):
    message = await ctx.channel.send(file=discord.File('images/kingbas.png'))
    heart_eyes = '\U0001F60D'
    await message.add_reaction(heart_eyes)


async def jewda(ctx):
    msg = discord.Embed(
        title="Jewda",
        color=0xFF5733
    )
    msg.set_image(url='https://pbs.twimg.com/profile_images/1223826538660974593/7Clo2xOB_400x400.jpg')
    await ctx.channel.send(embed=msg)


async def king(bot, ctx):
    msg = discord.Embed(
        title="You dropped something",
        color=0xFF5733
    )
    msg.set_author(
        name=ctx.bot.user.display_name,
        icon_url=ctx.bot.user.avatar_url
    )
    file = discord.File("images/heyking.gif", filename='king.gif')
    msg.set_image(url='attachment://king.gif')
    msg.set_footer(text='So handsome and smart. Look at that great smile! 👑')
    return await ctx.channel.send(file=file , embed=msg)
