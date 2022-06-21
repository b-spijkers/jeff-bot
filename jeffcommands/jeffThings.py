import discord


# just some random jeff commands/interactions

def spanish(author):
    insult = 'Fuck you in spanish' + author
    return insult


def el_gordo(author):
    msg = discord.Embed(
        title="This is what " + author.display_name + " looks like",
        description="Imagine not being able to see your penis"
    )
    msg.set_author(
        name=author,
        icon_url=author.avatar_url
    )
    msg.set_image(url='https://pbs.twimg.com/profile_images/1452468940404314114/oCO9SlPF_400x400.jpg')
    msg.set_footer(text="Mucho grande")
    return msg


def recognise(author):
    insult = 'Fuck you, ' + author
    return insult


def jeff():
    url = 'https://cdn.discordapp.com/attachments/278917012682440705/981852676201533501/ezgif-3-eff60a9fb7.gif'
    return url


async def jeffhonk(ctx):
    msg = discord.Embed(color=0xFF5733)
    msg.set_image(url='https://www.pngitem.com/pimgs/m/630-6301861_honk-honk-goose-hd-png-download.png')

    await ctx.channel.send(embed=msg)
