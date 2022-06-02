import discord


def spanish(author):
    insult = 'Fuck you in spanish' + author
    return insult


def el_gordo(author):
    msg = discord.Embed(
        title="This is what " + author.display_name + " looks like",
        description="Imagine not being able to see your penis"
    )
    msg.set_author(name=author,
                   icon_url=author.avatar_url)
    msg.set_image(url='https://img.iex.nl/uploads/2017/elgordo2_efc38044-abb2-4eda-82b0-477bae0e3303.jpg')
    msg.set_footer(text="Mucho grande")
    return msg


def recognise(author):
    insult = 'Fuck you, ' + author
    return insult


def jeff():
    url = 'https://cdn.discordapp.com/attachments/278917012682440705/981852676201533501/ezgif-3-eff60a9fb7.gif'
    return url
