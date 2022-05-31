import random

import discord
import foaas
import funnies
import jeffThings
import os

from discord.utils import find
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="#")


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Fuck')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'jeff' in message.content.lower():
        mentioned = str(message.author.mention)
        insult = jeffThings.recognise(mentioned)
        await message.channel.send(insult)

    if 'el hefe' in message.content.lower():
        mentioned = str(message.author.mention)
        insult = jeffThings.spanish(mentioned)
        await message.channel.send(insult)
    await bot.process_commands(message)


@bot.event
async def on_ready():
    print('{0.user}'.format(bot) + ' is online and ready')


# Returns a dad joke
@bot.command(
    help="Random dad joke from a library with with around 630 dad jokes",
    brief="Random dad joke"
)
async def dad(ctx):
    joke = funnies.dad()
    msg = discord.Embed(
        title="Funny joke",
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
    if ctx.message.mentions:
        insult = funnies.insult()
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + insult)
    else:
        insult = funnies.insult()
        await ctx.channel.send(ctx.author.mention + ' ' + insult)


# Because fuck you
@bot.command(
    help="Why? Because fuck you, that's why.",
    brief="Why? Because fuck you, that's why."
)
async def because(ctx):
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
    msg = discord.Embed(color=0xFF5733)
    msg.set_image(url='https://www.pngitem.com/pimgs/m/630-6301861_honk-honk-goose-hd-png-download.png')

    await ctx.channel.send(embed=msg)


@bot.command(
    help="Like jeff gives a fuck",
    brief="Jeff doesn't give a fuck"
)
async def give(ctx):
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
    if ctx.message.mentions:
        msg = foaas.cool(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.cool(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Too lazy to explain",
    brief="Fascinating story"
)
async def fasc(ctx):
    if ctx.message.mentions:
        msg = foaas.fasc(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.fasc(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Too lazy to explain",
    brief="Don't want to talk"
)
async def stop(ctx):
    if ctx.message.mentions:
        msg = foaas.stop(str(ctx.author.mention))
        await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
    else:
        msg = foaas.stop(str(ctx.author.mention))
        await ctx.channel.send(msg)


@bot.command(
    help="Too lazy to explain",
    brief="Tells you to fuck off in Yoda, must @mention someone"
)
async def yoda(ctx):
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
        await ctx.channel.send(error)


# Jewda
@bot.command(
    help="Jewda",
    brief="Jewda"
)
async def jooda(ctx):
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
    dumble = funnies.dumbledore(str(ctx.author.mention))
    await ctx.channel.send(dumble)


@bot.command(
    help="Too lazy to explain",
    brief="Kill someone"
)
async def kill(ctx):
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
            msg.set_image(url=gif)
        elif author_of_msg == victim:
            gif = funnies.kill(author_of_msg, str(ctx.message.mentions[0].id))
            msg = discord.Embed(
                description=str(ctx.author.mention) + ' commited suicide',
                color=discord.Color.red()
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
            ]
            gif = funnies.kill(author_of_msg, str(ctx.message.mentions[0].id))
            msg = discord.Embed(
                description=str(ctx.author.mention) + random.choice(killed_messages) + '<@' + str(ctx.message.mentions[0].id) + '>',
                color=discord.Color.blue()
            )
            msg.set_image(url=gif)
    else:
        msg = discord.Embed(
            title='Uh oh! Someone is retarded!',
            description='Must @mention someone you egg!',
            color=discord.Color.red()
        )

    await ctx.channel.send(embed=msg)


@bot.command()
async def nicht(ctx):
    vid = funnies.nicht()
    await ctx.channel.send(vid)


@bot.command()
async def b2ba(ctx):
    vid = funnies.b2ba()
    await ctx.channel.send(vid)

bot.run(DISCORD_TOKEN)
