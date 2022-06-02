import requests

from bs4 import BeautifulSoup


def wikilink():
    url = requests.get('https://en.uncyclopedia.co/wiki/Special:RandomRootpage/Main')
    soup = BeautifulSoup(url.content, 'html.parser')
    title_of_post = soup.find(class_="firstHeading").text

    return title_of_post

