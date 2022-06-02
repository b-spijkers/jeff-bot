import requests
import json


def useless_fact():
    response = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
    json_data = json.loads(response.text)
    fact = json_data['text']
    return fact


def next_episode(name):
    show = name.replace(" ", "-")
    response = requests.get('https://catchtheshow.herokuapp.com/api/' + show)
    json_data = json.loads(response.text)
    next_episode_data = json_data['nextEpisode']
    show_name = json_data['name']
    countdown = next_episode_data['countdown']

    return countdown, show_name
