import requests
import json


def recognise(author):
    insult = 'Fuck you, ' + author
    return insult


def dumbledore(author):
    response = requests.get('https://foaas.com/dumbledore/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    dumble = json_data['message']
    return dumble


def throw_yoda(name):
    yoda = 'Fuck off, you must, ' + name
    return yoda


def throw_give(author):
    response = requests.get('https://foaas.com/give/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    give = json_data['message']
    return give


def throw_fascinating(author):
    response = requests.get('https://foaas.com/fascinating/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    fascinating = json_data['message']
    return fascinating


def throw_cool(author):
    response = requests.get('https://foaas.com/cool/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    cool = json_data['message']
    return cool


def throw_because(author):
    response = requests.get('https://foaas.com/because/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    because = json_data['message']
    return because


def get_insult():
    response = requests.get('https://insult.mattbas.org/api/insult')
    insult = response.text
    return insult
