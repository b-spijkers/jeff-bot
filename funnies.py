import random
import requests
import json


# Just some commands I find funny or are just generally pretty fun


def dad():
    response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    joke = json_data['joke']
    return joke


def dumbledore(author):
    response = requests.get('https://foaas.com/dumbledore/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    msg = json_data['message']
    return msg


def yoda(name):
    yoda = 'Fuck off, you must, ' + name
    return yoda


def insult():
    response = requests.get('https://insult.mattbas.org/api/insult')
    insult = response.text
    return insult


def kill(author, victim):
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

    victim = '<@!' + victim + '>'

    if author == victim:
        gif = random.choice(suicide_gifs)
    else:
        gif = random.choice(kill_gifs)
    return gif


# Nicht rijder zooi, born 2 be alive is van The Village People, iedereen weet dat. Wat is een Patrick Hernandez? Idk
def nicht():
    return 'https://www.youtube.com/watch?v=Pie6izHuaMU'


def b2ba():
    return 'https://www.youtube.com/watch?v=YajODJwJhwk'
