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
        icon_url=bot.user.avatar_url
    )
    await ctx.channel.send(embed=msg)


def check_next_episode_status(name):
    show = '-'.join(name)
    response = requests.get('https://catchtheshow.herokuapp.com/api/' + show)
    json_data = json.loads(response.text)
    show_status = json_data['status']

    return show_status


def show_details(name):
    show = '-'.join(name)
    response = requests.get('https://catchtheshow.herokuapp.com/api/' + show)
    json_data = json.loads(response.text)
    show_status = json_data['status']

    if show_status == 'Canceled/Ended':
        show_name = json_data['name']
        return show_name, show_status
    else:
        show_name = json_data['name']
        next_episode_countdown = json_data['nextEpisode']['countdown']
        next_episode_day = json_data['nextEpisode']['date']['day']
        next_episode_month = json_data['nextEpisode']['date']['month']
        next_episode_year = json_data['nextEpisode']['date']['year']
        previous_episode_day = json_data['previousEpisode']['date']['day']
        previous_episode_month = json_data['previousEpisode']['date']['month']
        previous_episode_year = json_data['previousEpisode']['date']['year']

        months = {
            1 : 'Jan',
            2 : 'Feb',
            3 : 'Mar',
            4 : 'Apr',
            5 : 'May',
            6 : 'Jun',
            7 : 'Jul',
            8 : 'Aug',
            9 : 'Sep',
            10: 'Okt',
            11: 'Nov',
            12: 'Dec'
        }
        return show_name, next_episode_countdown, next_episode_day, months[next_episode_month], next_episode_year, previous_episode_day, \
            months[previous_episode_month], previous_episode_year


async def next_episode(ctx, args, bot):
    try:
        status = check_next_episode_status(args)

        if status != 'Canceled/Ended':
            try:
                name, countdown, next_day, next_month, next_year, prev_day, prev_month, prev_year = show_details(args)

                botConsole.log_command(ctx)

                msg = discord.Embed(
                    title=name,
                    description='Episode information',
                    color=discord.Color.blurple()
                )
                msg.add_field(
                    name="Prev. episode date:", value=str(prev_day) + ' ' + str(prev_month) + ' ' + str(prev_year),
                    inline=False
                )
                msg.add_field(
                    name="Next episode date: ", value=str(next_day) + ' ' + str(next_month) + ' ' + str(next_year),
                    inline=False
                )
                msg.add_field(
                    name="Countdown:", value=countdown,
                    inline=False
                )
                msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
                msg.set_author(
                    name=bot.user.display_name,
                    icon_url=bot.user.avatar_url
                )
                await ctx.channel.send(embed=msg)
            except Exception as e:
                print(e, '\n')
                await ctx.channel.send("Either i can't find the show or something else went wrong")
        else:
            try:
                name, status = show_details(args)

                botConsole.log_command(ctx)

                msg = discord.Embed(
                    title=name + ' - ' + status,
                    description='Show has ended or has been cancelled',
                    color=discord.Color.blurple()
                )
                msg.set_footer(text="Requested by: {}".format(ctx.author.display_name))
                msg.set_author(
                    name=bot.user.display_name,
                    icon_url=bot.user.avatar_url
                )
                await ctx.channel.send(embed=msg)
            except Exception as e:
                print(e, '\n')
                await ctx.channel.send("Either i can't find the show or something else went wrong")
    except Exception as ex:
        print(ex, '\n')
        await ctx.channel.send("API broke, this tends to happen A LOT")


def find_movie(name):
    name = '%20'.join(name)
    response = requests.get('https://imdb-api.com/en/API/SearchMovie/k_e4301r8z/' + name)
    json_data = json.loads(response.text)
    movieId = json_data['results'][0]['id']
    movieImg = json_data['results'][0]['image']
    return movieId, movieImg


def movie_data(movieId):
    response = requests.get('https://imdb-api.com/en/API/Ratings/k_e4301r8z/' + movieId)
    json_data = json.loads(response.text)
    movieTitle = json_data['fullTitle']
    imdbRating = json_data['imDb']
    metaRating = json_data['metacritic']
    tmdbRating = json_data['theMovieDb']
    rottRating = json_data['rottenTomatoes']
    filmRating = json_data['filmAffinity']
    return movieTitle, imdbRating, metaRating, tmdbRating, rottRating, filmRating


async def find_movie_results(ctx, args):
    movieId, movieImg = find_movie(args)
    movieTitle, imdbRating, metaRating, tmdbRating, rottRating, filmRating = movie_data(movieId)

    botConsole.log_command(ctx)

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


def find_show(name):
    name = '%20'.join(name)
    response = requests.get('https://imdb-api.com/en/API/SearchSeries/k_e4301r8z/' + name)
    json_data = json.loads(response.text)
    showId = json_data['results'][0]['id']
    showImg = json_data['results'][0]['image']
    return showId, showImg


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


async def joke_finder(bot, ctx, jokeType):
    msg = discord.Embed()
    if jokeType == 'misc':
        jokeType = 'Miscellaneous'

    response = requests.get('https://v2.jokeapi.dev/joke/' + jokeType)
    json_data = json.loads(response.text)
    joke_type = json_data['type']

    try:
        if joke_type == 'single':
            joke_setup = json_data['setup']
            joke_delivery = json_data['delivery']

            msg = discord.Embed(
                title=joke_setup,
                description=joke_delivery,
                color=0xFF5733,
            )
        elif joke_type == 'twopart':
            joke = json_data['joke']

            msg = discord.Embed(
                title=joke,
                color=0xFF5733,
            )
        msg.set_footer(
            text="Requested by: {}".format(
                ctx.author.display_name
            )
        )
        msg.set_author(
            name=bot.user.display_name,
            icon_url=bot.user.avatar_url
        )
        await ctx.channel.send(embed=msg)
    except Exception:
        await ctx.channel.send("Something went wrong... I've no idea why... Try again")
