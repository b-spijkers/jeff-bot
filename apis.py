import requests
import json


# Random API functions, most of the time just 1 or 2 functions per API
# It would seem unnecessary to split it up in multiple files


def useless_fact():
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    json_data = json.loads(response.text)
    fact = json_data['text']
    return fact


def check_next_episode_status(name):
    show = '-'.join(name)
    response = requests.get('https://catchtheshow.herokuapp.com/api/' + show)
    json_data = json.loads(response.text)
    show_status = json_data['status']

    return show_status


def next_episode(name):
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


def joke_finder(jokeType):
    if jokeType == 'misc':
        jokeType = 'Miscellaneous'

    response = requests.get('https://v2.jokeapi.dev/joke/' + jokeType)
    json_data = json.loads(response.text)
    joke_type = json_data['type']

    if joke_type == 'single':
        joke = json_data['joke']
        return joke
    elif joke_type == 'twopart':
        joke_setup = json_data['setup']
        joke_delivery = json_data['delivery']
        return joke_setup, joke_delivery
