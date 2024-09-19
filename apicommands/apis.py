import requests
import json
import discord

# Random API functions, most of the time just 1 or 2 functions per API
# It would seem unnecessary to split it up in multiple files
from botsettings import botConsole


async def useless_fact(ctx, bot):
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    json_data = json.loads(response.text)
    fact = json_data['text']
    fact.replace('"', "'")
    msg = discord.Embed(
        title="Random bullshit, GO!",
        description=fact,
        color=discord.Color.blurple()
    )
    msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    msg.set_author(
        name=bot.user.display_name,
        icon_url=bot.user.avatar
    )
    await ctx.channel.send(embed=msg)


def find_movie(name):
    name = '%20'.join(name)
    response = requests.get('https://search.imdbot.workers.dev/?q=' + name)
    json_data = json.loads(response.text)
    print(json_data)
    movieId = json_data['description'][0]['#IMDB_ID']
    movieImg = json_data['description'][0]['#IMG_POSTER']
    return movieId, movieImg


def movie_data(movieId):
    response = requests.get('https://search.imdbot.workers.dev/?tt=' + movieId)
    json_data = json.loads(response.text)
    movieTitle = json_data['short']['name']
    imdbRating = json_data['short']['aggregateRating']['ratingValue']
    imdbTrailer = json_data['short']['trailer']['embedUrl']
    return movieTitle, imdbRating, imdbTrailer


async def find_movie_results(ctx, args):
    movieId, movieImg = find_movie(args)
    movieTitle, imdbRating, imdbTrailer = movie_data(movieId)

    botConsole.log_command(ctx)

    msg = discord.Embed(
        title=movieTitle,
        color=discord.Color.orange()
    )
    msg.set_thumbnail(url=movieImg)
    msg.add_field(
        name="IMDb", value=imdbRating,
        inline=True
    )
    msg.add_field(
        name="Trailer", value=imdbTrailer,
        inline=True
    )
    msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    msg.set_author(
        name='IMDb',
        icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/640px-IMDB_Logo_2016.svg.png'
    )

    await ctx.channel.send(embed=msg)


# deprecated
def find_show(name):
    name = '%20'.join(name)
    response = requests.get('https://search.imdbot.workers.dev/?q=' + name)
    json_data = json.loads(response.text)
    showId = json_data['results'][0]['id']
    showImg = json_data['results'][0]['image']
    return showId, showImg


# deprecated
def show_data(movieId):
    response = requests.get('https://imdb-api.com/en/API/Ratings/k_e4301r8z/' + movieId)
    json_data = json.loads(response.text)
    showTitle = json_data['fullTitle']
    imdbRating = json_data['imDb']
    metaRating = json_data['metacritic']
    tmdbRating = json_data['theMovieDb']
    rottRating = json_data['rottenTomatoes']
    filmRating = json_data['filmAffinity']
    return showTitle, imdbRating, metaRating, tmdbRating, rottRating, filmRating


# deprecated
async def find_show_results(ctx, args):
    showId, showImg = find_show(args)
    showTitle, imdbRating, metaRating, tmdbRating, rottRating, filmRating = show_data(showId)

    botConsole.log_command(ctx)

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
    msg.set_footer(text="Data gathered from IMDb.")
    msg.set_author(
        name='IMDb',
        icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/640px-IMDB_Logo_2016.svg.png'
    )

    await ctx.channel.send(embed=msg)


# deprecated
async def joke_finder(bot, ctx, jokeType):
    msg = discord.Embed()
    if jokeType == 'misc':
        jokeType = 'Miscellaneous'
    print(jokeType)
    response = requests.get('https://v2.jokeapi.dev/joke/' + jokeType)
    json_data = json.loads(response.text)
    joke_type = json_data['type']
    print(json_data)
    try:
        if joke_type == 'single':
            joke_delivery = json_data['joke']

            msg = discord.Embed(
                title='This is a: ' + jokeType + ' joke.',
                description=joke_delivery,
                color=0xFF5733,
            )
        elif joke_type == 'twopart':
            joke_setup = json_data['setup']
            joke = json_data['delivery']

            msg = discord.Embed(
                title=joke_setup,
                description=joke,
                color=0xFF5733,
            )
        msg.set_footer(
            text="Requested by: {}".format(
                ctx.author.display_name
            )
        )
        msg.set_author(
            name=bot.user.display_name,
            icon_url=bot.user.avatar
        )
        await ctx.channel.send(embed=msg)
    except Exception:
        await ctx.channel.send("Something went wrong... I've no idea why... Try again...or don't.")
