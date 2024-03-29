#
#
# Note to self: Always update the help command if new commands are added. And always use OOP!
#
#
import asyncio
import datetime
import os
import time

import discord
from discord.ext import commands
from discord.utils import find

from botsettings import prefix, botConsole
from apicommands import apis, foaas, uncyclopedia, tweakers
from casinogames import casinoCommands
from jeffcommands import jeffThings, jeffFun, jeffHelp

DISCORD_TOKEN = os.getenv("TOKEN")


# Get current date and time for console prints
def date_time(self):
    current_time = datetime.datetime.date(self)
    return current_time


guild_prefix = '//'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=guild_prefix, intents=intents, help_command=None)
bot.remove_command('help')


##################
# Error handlers #
##################
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.channel.send('No such command. Fucker.')


###############################################################################################
# Jeff specific commands and listeners. Like specific words or to other really specific stuff #
###############################################################################################
class JeffThings(commands.Cog, name='Things Jeff does'):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == bot.user:
            return

        if 'el hefe' in message.content.lower():
            print(
                'Command: el hefe trigger \n',
                'User: ' + message.author.name + '\n',
                'Guild: ' + message.channel.guild.name + '\n',
                'Time: ' + time.strftime("%Y-%m-%d %H:%M")
            )
            mentioned = str(message.author.mention)
            insult = jeffThings.spanish(mentioned)
            await message.channel.send(insult)

        if 'el gordo' in message.content.lower():
            print(
                'Command: el gordo trigger \n',
                'User: ' + message.author.name + '\n',
                'Guild: ' + message.channel.guild.name + '\n',
                'Time: ' + time.strftime("%Y-%m-%d %H:%M")
            )
            mentioned = message.author
            insult = jeffThings.el_gordo(mentioned)
            await message.channel.send(message.author.mention)
            await message.channel.send(embed=insult)

        # if 'bas is gay!' in message.content.lower():
        #     print(
        #         'Command: PepeJs at it again \n',
        #         'User: ' + message.author.name + '\n',
        #         'Guild: ' + message.channel.guild.name + '\n',
        #         'Time: ' + time.strftime("%Y-%m-%d %H:%M")
        #     )
        #     await message.channel.send(str(message.author.mention) + ' Ur gay')
        # if 'owo' in message.content.lower():
        #     print(
        #         'Command: PepeJs at it again \n',
        #         'User: ' + message.author.name + '\n',
        #         'Guild: ' + message.channel.guild.name + '\n',
        #         'Time: ' + time.strftime("%Y-%m-%d %H:%M")
        #     )
        #     await message.channel.send('https://c.tenor.com/Ik-kENFloS0AAAAC/pepega-pepe-the-frog.gif')

    @commands.command(
        help="Jeff",
        brief="My name a Jeff"
    )
    async def jeff(self, ctx):
        botConsole.log_command(ctx)
        message = jeffThings.jeff()
        await ctx.channel.send(message)

    @commands.command(
        help="Honk. Aliases are: `honk`",
        brief="Honk [alias = `honk`]",
        aliases=['honk']
    )
    async def jeff_honk(self, ctx):
        botConsole.log_command(ctx)
        await jeffThings.jeffhonk(ctx)


# restart bot admin command method
def restart_bot(self):
    # python = sys.executable
    # os.execl(python, python, *sys.argv)
    try:
        self.bot.logout()
    except EnvironmentError as e:
        print(e)
        self.bot.clear()


#############################################################################
# Standard bot commands, most bots have these commands so mine does as well #
#############################################################################
class StandardBotCommands(commands.Cog, name='Basic Bot Commands'):
    def __init__(self, botClient):
        self.bot = botClient

    @commands.Cog.listener()
    async def on_ready(self):
        print('{0.user}'.format(bot) + ' is online and ready\n')
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name='the screams of the damned')
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send("Sup' fuckers. Use //help to check my commands. Use //prefix <new_prefix> to set a new prefix")

    @commands.Cog.listener()
    async def on_guild_join(self, message):  # when the bot joins the guild
        prefix.add_guild(message)

    @commands.Cog.listener()
    async def on_guild_remove(self, message):  # when the bot is removed from the guild
        prefix.remove_guild(message)

    @commands.command(
        help='Show info about Jeff-bot. Aliases are: `info`, `jeffinfo`',
        brief='Show info about Jeff-bot [Aliases = `info`, `jeffinfo`]',
        aliases=['info', 'jeffinfo']
    )
    async def jeff_info(self, ctx):
        await jeffHelp.jeff_info(self, ctx, bot)

    @commands.command()
    async def help(self, ctx):
        await jeffHelp.help(self, ctx, bot)

    @commands.command(
        pass_context=True,
        help="Change Jeff's prefix. Aliases are: `prefix`",
        brief="Type: <prefix> <new prefix>",
        aliases=['prefix']
    )
    @commands.has_permissions(administrator=True)  # ensure that only administrators can use this command
    async def set_prefix(self, ctx, *, newprefix: str = None):
        await prefix.new_prefix(ctx, newprefix)

    # Currently not working
    @commands.command(
        aliases=['restart', 'boop']
    )
    async def restart_bot(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.author.id == 273898204960129025:
            print('Restarting bot...\n')
            await ctx.send(
                "Restarting bot... should be back online in 5 sec. This message doesn't get removed or edited because I'm a dumbass..."
            )
            restart_bot(self)
        else:
            await ctx.send("Ur not Daddy BawonVonBawwon. U can't use this cummand. Sowwy OwO")


########################
# King Bas in da house #
########################
class Daddy(commands.Cog, name="OwO it's the king"):  # King Bas command, showing bas at his prime. What a king
    def __init__(self, botClient):
        self.bot = botClient

    @commands.command(
        help='Be blessed',
        aliases=['kingbas', 'bas']
    )
    async def king_bas(self, ctx):
        botConsole.log_command(ctx)
        await jeffFun.kingbas(ctx)


################
# Casino games #
################
class Casino(commands.Cog, name='Casino commands'):
    def __init__(self, botClient):
        self.bot = botClient

    @commands.command(
        help='By joining you are allowed to play blackjack(WIP) and other casino games that will be added later',
        aliases=['jc']
    )
    async def casino_join(self, ctx):
        botConsole.log_command(ctx)
        try:
            await casinoCommands.join_casino(ctx)
        except Exception as e:
            print(e)
            await ctx.channel.send('Something went wrong')

    @commands.command(
        help='Play a round of blackjack (WIP)',
        aliases=['bj', 'blackjack']
    )
    async def blackjack_play(self, ctx):
        botConsole.log_command(ctx)
        await ctx.channel.send('Blackjack is still being worked on (Not Actively). No idea when BaronVonBarron#7882 will be done...')

    @commands.command(
        help='Flip a coin and win',
        aliases=['cf', 'coinflip']
    )
    async def casino_coinflip(self, ctx, *args):
        botConsole.log_command(ctx)
        try:
            try:
                casinoCommands.check_entry(ctx.author.id)
            except Exception as e:
                print(e)
                return await ctx.channel.send('First you must register yourself. Use <prefix>jc')
            cf_result = casinoCommands.coinflip(ctx, args[0], args[1])
            await ctx.channel.send(cf_result)
        except Exception as e:
            print(e)
            await ctx.channel.send('Something went wrong, no idea what')

    @commands.command(
        help='Receive some help from the casino',
        aliases=['gib']
    )
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def casino_chip_gib(self, ctx):
        botConsole.log_command(ctx)
        await casinoCommands.casino_contribution(ctx)

    @casino_chip_gib.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(f'Casino is done giving you free chips. Ask again in {round(error.retry_after, 0)} seconds')

    @commands.command(
        aliases=['chips', 'ch', 'c']
    )
    async def check_chips(self, ctx):
        await casinoCommands.check_user_chips(ctx)


#############################################################
# Jeff's API commands, relates to all commands using an API #
#############################################################
class Api(commands.Cog, name='API commands'):
    def __init__(self, botClient):
        self.bot = botClient

    @commands.command(
        help='Random uncyclopedia article, which is probably horrible',
        aliases=['random', 'uncy']
    )
    async def uncyclopedia(self, ctx):
        botConsole.log_command(ctx)
        await uncyclopedia.uncyclopedia_post(bot, ctx)


    @commands.command(
        help='Most recent tweakers article, doesnt really work atm',
        aliases=['tweak']
    )
    async def tweakers(self, ctx):
        botConsole.log_command(ctx)
        await tweakers.tweakers_new_post(bot, ctx)


    # returns random joke
    @commands.command(
        help="Random joke, most are dark. Always specify type of joke. Joke types are: Programming, Misc, Dark, Pun, Spooky, Christmas",
        brief="Random joke, most are dark. And some are really racist",
        aliases=['joke']
    )
    async def get_joke(self, ctx, args):
        botConsole.log_command(ctx)
        await apis.joke_finder(bot, ctx, args)

    @get_joke.error
    async def joke_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):  # Check if the exception is Missing Required Argument
            await ctx.send(
                f"Please specify joke type. Like:<prefix>joke <joke_type>. Joke types are: Programming, Misc, Dark, Pun, Spooky, Christmas"
            )

    # Returns a dad joke
    @commands.command(
        help="Random dad joke from a library with around 630 dad jokes",
        brief="Random dad joke",
        aliases=['dad', 'dadjoke', 'djoke']
    )
    async def dad_joke(self, ctx):
        botConsole.log_command(ctx)
        await jeffFun.dad(ctx)

    # Returns air date of next episode of given show
    @commands.command(
        help="Shows when the next episode is supposed to air of given TV . Some show's might not me available",
        brief="<prefix>ne <title_of_show>",
        aliases=['ne', 'nextep', 'neep', 'nextepisode']
    )
    async def next_episode(self, ctx, *args):
        async with ctx.typing():
            await apis.next_episode(ctx, args, bot)

    @commands.command(
        help="<prefix>fm <title_of_movie>",
        brief="Gets movie score",
        aliases=['fm', 'findm', 'fmovie']
    )
    async def find_movie(self, ctx, *args):
        async with ctx.typing():
            await apis.find_movie_results(ctx, args)

    @commands.command(
        help="<prefix>fs <title_of_show>",
        brief="Gets show score",
        aliases=['fs', 'finds', 'fshow']
    )
    async def find_show(self, ctx, *args):
        async with ctx.typing():
            await apis.find_show_results(ctx, args)

    @commands.command(
        help="Gives you a random useless fact ",
        brief="Gives you a random useless fact",
        aliases=['fact']
    )
    async def give_fact(self, ctx):
        botConsole.log_command(ctx)
        await apis.useless_fact(ctx, bot)


##########################################################################
# Commands I think are pretty funny, so they fall under the Fun category #
##########################################################################
class Fun(commands.Cog, name='Fun commands'):
    def __init__(self, botClient):
        self.bot = botClient

    # Returns a random insult
    @commands.command(
        help="Returns a random insult which makes no sense pretty much all of the time",
        brief="Returns a random insult which makes no sense",
        aliases=['beadick', 'bad']
    )
    async def be_a_dick(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            insult = jeffFun.insult()
            async with ctx.typing():
                await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + insult)
        else:
            insult = jeffFun.insult()
            async with ctx.typing():
                await ctx.channel.send(ctx.author.mention + ' ' + insult)

    # Because fuck you
    @commands.command(
        aliases=['why', '?'],
        help="Why? Because fuck you, that's why.",
        brief="Why? Because fuck you, that's why."
    )
    async def thats_why(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            msg = foaas.because(str(ctx.author.mention))
            await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
        else:
            msg = foaas.because(str(ctx.author.mention))
            await ctx.channel.send(msg)

    @commands.command(
        help="Like jeff gives a fuck",
        brief="Jeff doesn't give a fuck",
        aliases=['dc', 'dcare']
    )
    async def jeff_no_care(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            msg = foaas.give(str(ctx.author.mention))
            await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
        else:
            msg = foaas.give(str(ctx.author.mention))
            await ctx.channel.send(msg)

    @commands.command(
        help="Cool story, bro",
        brief="Cool story, bro",
        aliases=['cool', 'cs']
    )
    async def cool_story(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            msg = foaas.cool(str(ctx.author.mention))
            await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
        else:
            msg = foaas.cool(str(ctx.author.mention))
            await ctx.channel.send(msg)

    @commands.command(
        help="Too lazy to explain",
        brief="Fascinating story",
        aliases=['fasc']
    )
    async def fascinating(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            msg = foaas.fascinating(str(ctx.author.mention))
            await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
        else:
            msg = foaas.fascinating(str(ctx.author.mention))
            await ctx.channel.send(msg)

    @commands.command(
        help="Too lazy to explain",
        brief="Don't want to talk"
    )
    async def stop(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            msg = foaas.stop(str(ctx.author.mention))
            await ctx.channel.send('<@' + str(ctx.message.mentions[0].id) + '> ' + msg)
        else:
            msg = foaas.stop(str(ctx.author.mention))
            await ctx.channel.send(msg)

    @commands.command(
        help="Too lazy to explain",
        brief="Tells you to fuck off like he's yoda, must @mention someone",
        aliases=['yoda']
    )
    async def yoda_fuckoff(self, ctx):
        botConsole.log_command(ctx)
        if bot.user.mentioned_in(ctx.message):
            await ctx.channel.send('Fuck you')
        elif ctx.message.mentions:
            mentioned = '<@' + str(ctx.message.mentions[0].id) + '>'
            msg = jeffFun.yoda(mentioned)
            await ctx.channel.send(msg)
        else:
            if '#yoda <@mention>' in ctx.message.content:
                error = 'Very funny, asshole'
            else:
                error = 'Good job, idiot. Command is `<prefix>yoda <@mention>`'
            await ctx.channel.send(error, delete_after=10)

    # Jewda
    @commands.command(
        help="Jewda",
        brief="Jewda",
        aliases=['jooda', 'jewda']
    )
    async def yoda_jew(self, ctx):
        botConsole.log_command(ctx)
        await jeffFun.jewda(ctx)

    @commands.command(
        help="Too lazy to explain",
        brief="Too lazy to explain",
        aliases=['dumble', 'dumbledore']
    )
    async def wise_dumbledore(self, ctx):
        botConsole.log_command(ctx)
        await jeffFun.dumbledore(ctx)

    @commands.command(
        help="Too lazy to explain",
        brief="Kill someone or everyone",
        aliases=['kill']
    )
    async def kill_user(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            await jeffFun.kill(bot, ctx)
        elif '@everyone' in ctx.message.content:
            await jeffFun.kill_everyone(bot, ctx)
        else:
            await jeffFun.kill_none(ctx)

    @commands.command()
    async def nicht(self, ctx):
        botConsole.log_command(ctx)
        vid = jeffFun.nicht()
        await ctx.channel.send(vid)

    @commands.command()
    async def b2ba(self, ctx):
        botConsole.log_command(ctx)
        vid = jeffFun.b2ba()
        await ctx.channel.send(vid)

    @commands.command()
    async def king(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            await ctx.channel.send('Hey! <@' + str(ctx.message.mentions[0].id) + '> ...')
            await jeffFun.king(bot, ctx)
        else:
            await ctx.channel.send('Hey! ' + str(ctx.author.mention) + '...')
            await jeffFun.king(bot, ctx)

    @commands.command(
        aliases=['rip']
    )
    async def rest_in_peace(self, ctx):
        botConsole.log_command(ctx)
        if ctx.message.mentions:
            msg = discord.Embed(
                title='This man is fucking dead',
                description='<@' + str(ctx.message.mentions[0].id) + '>' + ' fucking died',
                color=discord.Color.orange()
            )
            msg.set_image(url='https://c.tenor.com/oUvaabzjR3gAAAAd/rip-coffin.gif')
            msg.set_footer(text='He fucking died')
            await ctx.send(embed=msg)
        else:
            msg = discord.Embed(
                title='This man is fucking dead',
                description=ctx.author.mention + ' fucking died',
                color=discord.Color.orange()
            )
            msg.set_image(url='https://c.tenor.com/oUvaabzjR3gAAAAd/rip-coffin.gif')
            msg.set_footer(text='He fucking died')
            await ctx.send(embed=msg)


async def main():
    async with bot:
        await bot.add_cog(StandardBotCommands(bot))
        await bot.add_cog(Api(bot))
        await bot.add_cog(Daddy(bot))
        await bot.add_cog(JeffThings(bot))
        await bot.add_cog(Casino(bot))
        await bot.add_cog(Fun(bot))
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
