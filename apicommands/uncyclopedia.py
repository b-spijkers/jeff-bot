import requests
import discord
import asyncio

from bs4 import BeautifulSoup


async def uncyclopedia_post(bot, ctx):
    url = requests.get('https://en.uncyclopedia.co/wiki/Special:RandomRootpage/Main')
    soup = BeautifulSoup(url.content, 'html.parser')
    title_of_post = soup.find(class_="firstHeading").text

    embed = discord.Embed(
        title="Title: " + title_of_post,
        description="Want to view this article?",
        color=discord.Color.blue()
    )
    embed.set_author(
        name="Uncyclopedia", url="https://en.uncyclopedia.co/",
        icon_url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png"
    )
    embed.set_thumbnail(url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png")
    embed.add_field(
        name="What do?", value="Sends a link on thumbs up. Removes the message on thumbs down.",
        inline=False
    )
    embed.set_footer(
        text="Requested by: {}".format(
            ctx.author.display_name
        ) + ". Jeff has worked very very hard to send you this message."
    )

    message = await ctx.send(embed=embed, delete_after=10)

    thumb_up = '👍'
    thumb_down = '👎'

    await message.add_reaction(thumb_up)
    await message.add_reaction(thumb_down)

    def check(reaction, user):
        return user == ctx.author and str(
            reaction.emoji
        ) in [thumb_up, thumb_down]

    member = ctx.author

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=10.0, check=check)

            if str(reaction.emoji) == thumb_up:
                post = title_of_post.replace(" ", "_")
                url = "https://en.uncyclopedia.co/wiki/%s" % post
                embed = discord.Embed(
                    title=title_of_post,
                    description=url,
                    color=discord.Color.blue()
                )
                embed.set_author(
                    name="Uncyclopedia", url="https://en.uncyclopedia.co/",
                    icon_url="https://images.uncyclomedia.co/uncyclopedia/en/b/bc/Wiki.png"
                )
                embed.set_footer(text="Stolen from Uncyclopedia for your entertainment")
                await message.delete()
                await ctx.send(embed=embed)
                break
            if str(reaction.emoji) == thumb_down:
                await message.delete()
                await ctx.send("Asshole", delete_after=10)
                break
        except asyncio.TimeoutError:
            await ctx.send("I don't have all day....", delete_after=10)
            break

