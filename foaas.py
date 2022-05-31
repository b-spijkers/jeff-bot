import requests
import json


def give(author):
    response = requests.get('https://foaas.com/give/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    give = json_data['message']
    return give


def fasc(author):
    response = requests.get('https://foaas.com/fascinating/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    fascinating = json_data['message']
    return fascinating


def cool(author):
    response = requests.get('https://foaas.com/cool/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    cool = json_data['message']
    return cool


def because(author):
    response = requests.get('https://foaas.com/because/' + author + '', headers={"Accept": "application/json"})
    json_data = json.loads(response.text)
    because = json_data['message']
    return because
