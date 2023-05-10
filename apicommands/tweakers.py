import requests
import discord
import asyncio

from bs4 import BeautifulSoup


async def tweakers_new_post(bot, ctx):
    url = requests.get('https://tweakers.net/')
    img = "https://tweakers.net/ext/i/2000677500.jpeg"
    soup = BeautifulSoup(url.content, 'html.parser')
    headline = soup.find(class_="headline")
    first_article = headline.select_one('a')
    title_of_post = first_article.text
    type_of_news = headline.findAll(True, {'class': ['sprite', 'contentIcon', 'pro', 'news']})[0].text

    embed = discord.Embed(
        title=title_of_post,
        description=type_of_news,
        color=discord.Color.blue()
    )
    embed.set_author(
        name="Tweakers", url="https://tweakers.net/",
        icon_url=img
    )
    embed.set_thumbnail(url=img)
    embed.set_footer(
        text="Requested by: {}".format(
            ctx.author.display_name
        ) + ". This is still very much work in progress."
    )

    return await ctx.send(embed=embed)
