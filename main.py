import asyncio
import datetime
import json
import os
import random
import sys
import time

import discord
from discord.ext import commands
from discord.utils import find
from dotenv import load_dotenv

import apis
import foaas
import funnies
import jeffThings
import uncyclopedia

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")


def date_time(self):
    current_time = datetime.datetime.date(self)
    return current_time


def get_prefix(bot, message):  # first we define get_prefix
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]  # receive the prefix for the guild id given


bot = commands.Bot(command_prefix=get_prefix)


@bot.event
async def on_ready():
    print('{0.user}'.format(bot) + ' is online and ready')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name='humans from his pond')
    )


@bot.event
async def on_guild_join(guild):  # when the bot joins the guild
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '//'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):  # when the bot is removed from the guild
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))  # find the guild.id that bot was removed from

    with open('prefixes.json', 'w') as f:  # deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)


@bot.command(
    pass_context=True,
    help="Change Jeff's prefix",
    brief="Type: <prefix> <new prefix>"
)
@commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
async def prefix(ctx, *, prefix: str = None):
    if prefix is None:
        print(
            'Command: change prefix failed \n',
            'User: ' + ctx.message.author.name + '\n',
            'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
            'Time: ' + time.strftime(
                "%Y-%m-%d %H:%M"
            )
        )
        return await ctx.send(f'Please set a new prefix by typing the new prefix after the command')
    else:
        print(
            'Command: changed prefix \n',
            'User: ' + ctx.message.author.name + '\n',
            'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
            'Time: ' + time.strftime(
                "%Y-%m-%d %H:%M"
            )
        )
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:  # writes the new prefix into the .json
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix changed to: {prefix}')  # confirms the prefix it's been changed to


@bot.command(
    name='random',
    help='Random uncyclopedia article, which is probably horrible'
)
async def pedia(ctx):
    global reaction

    print(
        'Command: Uncyclopedia article \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )

    title_of_post = uncyclopedia.wikilink()
    embed = discord.Embed(
        title="Title: " + title_of_post,
        description="Want to view this article?",
        color=discord.Color.blue()
    )
    embed.set_author(
        name="Uncyclopedia", url="https://en.uncyclopedia.co/",
        icon_url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png"
    )
    embed.set_thumbnail(url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png")
    embed.add_field(
        name="What do?", value="Sends a link on thumbs up. Removes the message on thumbs down.",
        inline=False
    )
    embed.set_footer(
        text="Requested by: {}".format(
            ctx.author.display_name
        ) + ". Jeff has worked very very hard to send you this message."
    )

    message = await ctx.send(embed=embed, delete_after=10)

    thumb_up = '👍'
    thumb_down = '👎'

    await message.add_reaction(thumb_up)
    await message.add_reaction(thumb_down)

    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji
        ) in [thumb_up, thumb_down]

    member = ctx.author

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.send("I don't have all day....", delete_after=10)

        if str(reaction.emoji) == thumb_up:
            post = title_of_post.replace(" ", "_")
            url = "https://en.uncyclopedia.co/wiki/%s" % post
            embed = discord.Embed(
                title=title_of_post,
                description=url,
                color=discord.Color.blue()
            )
            embed.set_author(
                name="Uncyclopedia", url="https://en.uncyclopedia.co/",
                icon_url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png"
            )
            embed.set_footer(text="Stolen from Uncyclopedia for your entertainment")
            await message.delete()
            await ctx.send(embed=embed)
        if str(reaction.emoji) == thumb_down:
            await message.delete()
            await ctx.send("Asshole", delete_after=10)


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Sup' fuckers. Use //help to check my commands. Use //prefix to set a new prefix")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'el hefe' in message.content.lower():
        print(
            'Command: el hefe trigger \n',
            'User: ' + message.author.name + '\n',
            'Guild: ' + message.channel.guild.name + '\n',
            'Time: ' + time.strftime("%Y-%m-%d %H:%M")
        )
        mentioned = str(message.author.mention)
        insult = jeffThings.spanish(mentioned)
        await message.channel.send(insult)

    if 'el gordo' in message.content.lower():
        print(
            'Command: el gordo trigger \n',
            'User: ' + message.author.name + '\n',
            'Guild: ' + message.channel.guild.name + '\n',
            'Time: ' + time.strftime("%Y-%m-%d %H:%M")
        )
        mentioned = message.author
        insult = jeffThings.el_gordo(mentioned)
        insult.set_image(url='https://img.iex.nl/uploads/2017/elgordo2_efc38044-abb2-4eda-82b0-477bae0e3303.jpg')
        await message.channel.send(message.author.mention)
        await message.channel.send(embed=insult)

    await bot.process_commands(message)


@bot.command(
    help="Jeff",
    brief="My name a Jeff"
)
async def jeff(ctx):
    print(
        'Command: my name a jeff \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    message = jeffThings.jeff()
    await ctx.channel.send(message)


# Returns a dad joke
@bot.command(
    help="Random dad joke from a library with around 630 dad jokes",
    brief="Random dad joke"
)
async def dad(ctx):
    print(
        'Command: dad \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    joke = funnies.dad()
    msg = discord.Embed(
        title="Hi, I'm dad",
        description=joke,
        color=0xFF5733,
    )
    await ctx.channel.send(embed=msg)


# Returns a random insult
@bot.command(
    help="Returns a random insult which makes no sense pretty much all of the time",
    brief="Returns a random insult which makes no sense"
)
async def beadick(ctx):
    print(
        'Command: be a dick \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        insult = funnies.insult()
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + insult)
    else:
        insult = funnies.insult()
        await ctx.channel.send(ctx.author.mention + ' ' + insult)


# Because fuck you
@bot.command(
    name="why",
    help="Why? Because fuck you, that's why.",
    brief="Why? Because fuck you, that's why."
)
async def because(ctx):
    print(
        'Command: because \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        msg = foaas.because(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.because(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Honk",
    brief="Honk"
)
async def honk(ctx):
    print(
        'Command: honk \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    msg = discord.Embed(color=0xFF5733)
    msg.set_image(url='https://www.pngitem.com/pimgs/m/630-6301861_honk-honk-goose-hd-png-download.png')

    await ctx.channel.send(embed=msg, delete_after=10)


@bot.command(
    help="Like jeff gives a fuck",
    brief="Jeff doesn't give a fuck"
)
async def give(ctx):
    print(
        'Command: give \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        msg = foaas.give(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.give(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Cool story, bro",
    brief="Cool story, bro"
)
async def cool(ctx):
    print(
        'Command: cool \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        msg = foaas.cool(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.cool(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Too lazy to explain",
    brief="Fascinating story",
    name='fasc'
)
async def fascinating(ctx):
    print(
        'Command: fascinating \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        msg = foaas.fascinating(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.fascinating(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Too lazy to explain",
    brief="Don't want to talk"
)
async def stop(ctx):
    print(
        'Command: stop \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        msg = foaas.stop(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.stop(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Too lazy to explain",
    brief="Tells you to fuck off like he's yoda, must @mention someone"
)
async def yoda(ctx):
    print(
        'Command: yoda \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if bot.user.mentioned_in(ctx.message):
        await ctx.channel.send('Fuck you')
    elif ctx.message.mentions:
        mentioned = '<@' + str(ctx.message.mentions[0].id) + '>'
        msg = funnies.yoda(mentioned)
        await ctx.channel.send(msg)
    else:
        if '#yoda <@mention>' in ctx.message.content:
            error = 'Very funny, asshole'
        else:
            error = 'Good job, idiot. Command is `#yoda <@mention>`'
        await ctx.channel.send(error, delete_after=10)


# Jewda
@bot.command(
    help="Jewda",
    brief="Jewda",
    name="jooda"
)
async def jewda(ctx):
    print(
        'Command: jewda \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    msg = discord.Embed(
        title="Jewda",
        color=0xFF5733
    )
    msg.set_image(url='https://pbs.twimg.com/profile_images/1223826538660974593/7Clo2xOB_400x400.jpg')
    await ctx.channel.send(embed=msg)


@bot.command(
    help="Too lazy to explain",
    brief="Too lazy to explain"
)
async def dum(ctx):
    print(
        'Command: dumbledore \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    dumble = funnies.dumbledore(str(ctx.author.mention))
    await ctx.channel.send(dumble)


@bot.command(
    help="Too lazy to explain",
    brief="Kill someone or everyone"
)
async def kill(ctx):
    print(
        'Command: kill \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    if ctx.message.mentions:
        author_of_msg = str(ctx.author.mention)
        victim = '<@!' + str(ctx.message.mentions[0].id) + '>'

        if '!' not in author_of_msg:
            author = author_of_msg[:2] + '!' + author_of_msg[2:]
            author_of_msg = author

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
        elif author_of_msg == victim:
            suicide_messages = [
                ' robloxed themselves',
                ' committed neck rope',
                ' game overed themselves',
                ' wasted themselves'
            ]
            gif = funnies.kill(author_of_msg, str(ctx.message.mentions[0].id))
            msg = discord.Embed(
                description=str(ctx.author.mention) + random.choice(suicide_messages),
                color=discord.Color.red()
            )
            msg.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url
            )
            msg.set_image(url=gif)
        else:
            killed_messages = [
                ' brutalized ',
                ' murdered ',
                ' rekt ',
                ' game overed ',
                ' fucked up ',
                ' terminated ',
                ' killed ',
                ' wasted '
                " KO'd "
            ]
            gif = funnies.kill(author_of_msg, str(ctx.message.mentions[0].id))
            msg = discord.Embed(
                description=str(ctx.author.mention) + random.choice(killed_messages) + '<@' + str(
                    ctx.message.mentions[0].id
                ) + '>',
                color=discord.Color.blue()
            )
            msg.set_image(url=gif)
    elif '@everyone' in ctx.message.content:
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
    else:
        msg = discord.Embed(
            title='Uh oh! Someone is retarded!',
            description='Must @mention someone you egg!',
            color=discord.Color.red()
        )

    await ctx.channel.send(embed=msg)


@bot.command()
async def nicht(ctx):
    print(
        'Command: nicht rijder \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    vid = funnies.nicht()
    await ctx.channel.send(vid)


@bot.command()
async def b2ba(ctx):
    print(
        'Command: born 2 be alive \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    vid = funnies.b2ba()
    await ctx.channel.send(vid)


@bot.command(
    help="Gives you a random useless fact",
    brief="Gives you a random useless fact"
)
async def fact(ctx):
    print(
        'Command: fact \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )
    useless_fact = apis.useless_fact()
    useless_fact.replace('"', "'")
    msg = discord.Embed(
        title="Random bullshit, GO!",
        description=useless_fact,
        color=discord.Color.blurple()
    )
    msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    msg.set_author(
        name=bot.user.display_name,
        icon_url=bot.user.avatar_url
    )

    await ctx.channel.send(embed=msg)


@bot.command(
    help="Shows when the next episode is supposed to air of given TV show",
    brief="<prefix>ne <title_of_show>",
    name="ne"
)
async def next_episode(ctx, *args):
    name = apis.next_episode(args)

    print(
        'Command: next_episode \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )

    msg = discord.Embed(
        title=name,
        description='',
        color=discord.Color.blurple()
    )
    msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    msg.set_author(
        name=bot.user.display_name,
        icon_url=bot.user.avatar_url
    )

    await ctx.channel.send(embed=msg)


@bot.command(
    help="<prefix>fm <title_of_movie>",
    brief="Gets movie score",
    name="fm"
)
async def find_movie(ctx, *args):
    movieId, movieImg = apis.find_movie(args)
    movieTitle, imdbRating, metaRating, tmdbRating, rottRating, filmRating = apis.movie_data(movieId)

    print(
        'Command: find_movie \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )

    msg = discord.Embed(
        title=movieTitle,
        description='Movie ratings:',
        color=discord.Color.orange()
    )
    msg.set_thumbnail(url=movieImg)
    msg.add_field(
        name="IMDb", value=imdbRating,
        inline=True
    )
    msg.add_field(
        name="Metacritic", value=metaRating,
        inline=True
    )
    msg.add_field(
        name="The Movie Db", value=tmdbRating,
        inline=True
    )
    msg.add_field(
        name="Rotten Tomatoes", value=rottRating,
        inline=True
    )
    msg.add_field(
        name="Film Affinity", value=filmRating,
        inline=True
    )
    msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    msg.set_author(
        name='IMDb',
        icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/640px-IMDB_Logo_2016.svg.png'
    )

    await ctx.channel.send(embed=msg)


@bot.command(
    help="<prefix>fs <title_of_show>",
    brief="Gets show score",
    name="fs"
)
async def find_show(ctx, *args):
    showId, showImg = apis.find_show(args)
    showTitle, imdbRating, metaRating, tmdbRating, rottRating, filmRating = apis.show_data(showId)

    print(
        'Command: find_show \n',
        'User: ' + ctx.message.author.name + '\n',
        'Guild: ' + ctx.channel.guild.name + '\n', 'Guild ID: ' + str(ctx.channel.guild.id) + '\n',
        'Time: ' + time.strftime("%Y-%m-%d %H:%M \n")
    )

    msg = discord.Embed(
        title=showTitle,
        description='Show ratings:',
        color=discord.Color.orange()
    )
    msg.set_thumbnail(url=showImg)
    msg.add_field(
        name="IMDb", value=imdbRating,
        inline=True
    )
    msg.add_field(
        name="Metacritic", value=metaRating,
        inline=True
    )
    msg.add_field(
        name="The Movie Db", value=tmdbRating,
        inline=True
    )
    msg.add_field(
        name="Rotten Tomatoes", value=rottRating,
        inline=True
    )
    msg.add_field(
        name="Film Affinity", value=filmRating,
        inline=True
    )
    msg.set_footer(text="Data gathered from IMDb.")
    msg.set_author(
        name='IMDb',
        icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/640px-IMDB_Logo_2016.svg.png'
    )

    await ctx.channel.send(embed=msg)


# restart bot admin command

def restart_bot():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@bot.command(
    name='restart',
    brief='Restarts the bot'
)
async def restart(ctx):
    if ctx.message.author.id == 273898204960129025:
        print('Restarting bot...')
        await ctx.send("Restarting bot...")
        restart_bot()
    else:
        await ctx.send("Ur not Daddy BawonVonBawwon. U can't use this cummand. Sowwy OwO (i wanna die)")


bot.run(DISCORD_TOKEN)
