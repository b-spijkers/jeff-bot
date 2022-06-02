import asyncio
import os
import random

import discord
from discord.ext import commands
from discord.utils import find
from dotenv import load_dotenv

import foaas
import funnies
import jeffThings
import uncyclopedia

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="#")


@bot.command(name='random', help='Random uncyclopedia article, which is probably horrible')
async def pedia(ctx):
    global reaction

    title_of_post = uncyclopedia.wikilink()
    embed = discord.Embed(
        title="Title: " + title_of_post,
        description="Want to view this article?",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png")
    embed.add_field(name="What do?", value="Sends a link on thumbs up. Removes the message on thumbs down.",
                    inline=False)
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name) + ". Jeff has worked very very hard to send you this message.")

    message = await ctx.send(embed=embed)

    thumb_up = '👍'
    thumb_down = '👎'

    await message.add_reaction(thumb_up)
    await message.add_reaction(thumb_down)

    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji) in [thumb_up, thumb_down]

    member = ctx.author

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await message.delete()
            await ctx.send("I don't have all day....", delete_after=10)

        if str(reaction.emoji) == thumb_up:
            post = title_of_post.replace(" ", "_")
            url = "https://en.uncyclopedia.co/wiki/%s" % post
            embed = discord.Embed(
                title='Here you go',
                description=url,
                color=discord.Color.blue()
            )
            await message.delete()
            await ctx.send(embed=embed)
        if str(reaction.emoji) == thumb_down:
            await message.delete()
            await ctx.send("Asshole", delete_after=10)


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Sup' fuckers")
        await general.send("My prefix can't be changed. The dude that made me still too dumb to add that feature")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

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
    name="why",
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

    await ctx.channel.send(embed=msg, delete_after=10)


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
    brief="Tells you to fuck off like he's yoda, must @mention someone"
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
        await ctx.channel.send(error, delete_after=10)


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
    brief="Kill someone or everyone"
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
                description=str(ctx.author.mention) + random.choice(killed_messages) + '<@' + str(
                    ctx.message.mentions[0].id) + '>',
                color=discord.Color.blue()
            )
            msg.set_image(url=gif)
    elif '@everyone' in ctx.message.content:
        msg = discord.Embed(
            description="Jeff is done with this planet"
        )
        msg.set_footer(text="Requested by: {}".format(
            ctx.author.display_name) + ". Jeff has always wanted to do this")
        msg.set_image(url='https://c.tenor.com/RjAxaS7VppAAAAAC/deathstar.gif')
        # msg.set_thumbnail(url='https://i.imgflip.com/4bdfem.png')
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
