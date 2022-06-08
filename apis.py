import requests
import json


# Random API functions, most of the time just 1 or 2 functions per API
# It would seem unnecessary to split it up in multiple files


def useless_fact():
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    json_data = json.loads(response.text)
    fact = json_data['text']
    return fact


def next_episode(name):
    show = '-'.join(name)
    response = requests.get('https://catchtheshow.herokuapp.com/api/' + show)
    json_data = json.loads(response.json())
    show_name = json_data['name']
    return show_name


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