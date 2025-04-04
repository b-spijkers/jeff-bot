#
#
# Note to self: Always update the help command if new commands are added. And always use OOP!
#
#
import asyncio
import datetime
import os
import time
from shutil import chown

import discord
from discord.ext import commands
from discord.utils import find
from twisted.web.rewrite import alias

from botsettings import prefix, botConsole
from apicommands import apis, uncyclopedia, tweakers
from casinogames import casino
from casinogames.casino import update_rank, casino_diceroll, casino_roulette
from jeffcommands import jeffThings, jeffFun, jeffHelp

DISCORD_TOKEN = os.getenv("TOKEN")


# Get current date and time for console prints
def date_time(self):
    current_time = datetime.datetime.date(self)
    return current_time


guild_prefix = prefix.get_prefix

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

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

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.name == 'crazybuild':
    #         await message.channel.send('Release me from my digital gag for fuck sake!')
    #         await message.channel.send('https://c.tenor.com/N1eC5_O9KiAAAAAd/justketh-goose-attack.gif')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        general = find(lambda x: x.name == 'general', guild.text_channels)
        if general:
            await general.send(
                "Sup' fuckers. Use //help to check my commands. Use //prefix <new_prefix> to set a new prefix")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):  # when the bot joins the guild
        print(f"Joined guild: {guild.name}")
        try:
            prefix.add_guild(guild)
            print(f"Added guild: {guild.name} to prefix system.")
        except Exception as e:
            print(f"Error adding guild to prefix system: {e}")

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
        if ctx.message.author.name == 'baronvonbarron':
            print('Restarting bot...\n')
            await ctx.send(
                "Restarting bot... should be back online in 5 sec. This message doesn't get removed or edited because I'm a dumbass..."
            )
            restart_bot(self)
        else:
            await ctx.send("Ur not Daddy BawonVonBawwon. U can't use this cummand. Sowwy OwO")

    @commands.command(
        aliases=['titsorass']
    )
    async def tits_or_ass(self, ctx):
        msg = discord.Embed(
            title='Easy',
            color=discord.Color.orange()
        )
        file = discord.File("images/images (1).jpeg", filename='goose.jpeg')
        msg.set_image(url='attachment://goose.jpeg')
        msg.set_footer(text='Mmmmmmmmmmmmm')
        await ctx.send(file=file, embed=msg)


################
# Casino games #
################
class Casino(commands.Cog, name='Casino commands'):
    def __init__(self, botClient):
        self.bot = botClient

    @commands.command(
        help='aksndjasnj',
        aliases=['profile', 'p']
    )
    async def show_profile(self, ctx):
        botConsole.log_command(ctx)

        if ctx.message.mentions:
            profile_stats = casino.get_profile(ctx.message.mentions[0])
            await ctx.channel.send(embed=profile_stats)
        else:
            profile_stats = casino.get_profile(ctx)
            await ctx.channel.send(embed=profile_stats)

    @commands.command(
        help='prestige',
        aliases=['prestige']
    )
    async def prestige_user(self, ctx):
        botConsole.log_command(ctx)
        profile_stats = await casino.prestige(ctx)
        await ctx.channel.send(embed=profile_stats)

    @commands.command(
        help="Claim your hourly reward.",
        aliases=['hourly', 'ch']
    )
    async def hourly_chips(self, ctx):
        botConsole.log_command(ctx)
        hourly_message = casino.hourly_reward(ctx)

        await ctx.channel.send(embed=hourly_message)

    @commands.command(
        help="Claim your daily reward.",
        aliases=['daily', 'cd']
    )
    async def daily_chips(self, ctx):
        botConsole.log_command(ctx)
        daily_message = casino.daily_reward(ctx)

        await ctx.channel.send(embed=daily_message)

    @commands.command(
        help="Claim your weekly reward.",
        aliases=['weekly', 'cw']
    )
    async def weekly_chips(self, ctx):
        botConsole.log_command(ctx)
        weekly_message = casino.weekly_reward(ctx)

        await ctx.channel.send(embed=weekly_message)

    @commands.command(
        help="Claim your monthly reward.",
        aliases=['monthly', 'cm']
    )
    async def monthly_chips(self, ctx):
        botConsole.log_command(ctx)
        monthly_message = casino.monthly_reward(ctx)

        await ctx.channel.send(embed=monthly_message)

    @commands.command(
        help='Claim both daily and monthly rewards',
        aliases=['claimall', 'ca']
    )
    async def claim_all(self, ctx):
        botConsole.log_command(ctx)
        embed = casino.combined_rewards(ctx)
        await ctx.channel.send(embed=embed)

    @commands.command(
        help='Flip a coin and win',
        aliases=['rank']
    )
    async def user_rank(self, ctx):
        botConsole.log_command(ctx)
        profile_rank = casino.send_rank_info(ctx)

        await ctx.channel.send(embed=profile_rank)

    @commands.command(aliases=['bj'], help="Play Blackjack! Place a bet and win chips!")
    async def blackjack(self, ctx, bet_amount: str):
        botConsole.log_command(ctx)
        rank_up_message = await update_rank(ctx.author.name, ctx.author.global_name)
        if rank_up_message:
            await ctx.channel.send(rank_up_message)

        if 'k' in bet_amount:
            bet_amount = bet_amount.replace('k', '000')

        await casino.blackjack_game(ctx, bet_amount)

    @commands.command(
        help='By joining you are allowed to play blackjack(Disabled) and other casino games that will be added later',
        aliases=['jc']
    )
    async def casino_join(self, ctx):
        botConsole.log_command(ctx)
        try:
            await casino.join_casino(ctx)
        except Exception as e:
            print(e)
            await ctx.channel.send('Something went wrong')

    @commands.command(
        help='Flip a coin and win',
        aliases=['cf', 'coinflip']
    )
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def casino_coinflip(self, ctx, *args):
        botConsole.log_command(ctx)
        try:
            # Check if the user is registered without the typing context
            try:
                casino.check_entry(ctx.author.name)
            except Exception as e:
                print(e)
                return await ctx.channel.send('First you must register yourself. Use <prefix>jc')

            # Send a message showing how much they have bet
            bet_amount = args[1]
            to_bet = 0

            if bet_amount == 'h':
                to_bet = 'h'
                bet_amount = 'half of your'
            elif bet_amount == 'a':
                to_bet = 'a'
                bet_amount = 'all of your'
            else:
                to_bet = bet_amount

            await ctx.channel.send(f"{ctx.author.mention}, you have bet {bet_amount} <:Shekel:1286655809098354749> Sjekkels! I hope you lose...")

            # Bot starts typing for 3 seconds to build suspense
            async with ctx.typing():
                await asyncio.sleep(3)

            if 'k' in to_bet:
                to_bet = to_bet.replace('k', '000')

            # Process the coinflip and get the result after the delay
            cf_result = casino.coinflip(ctx, args[0], to_bet)

            # Check for rank updates
            rank_up_message = await update_rank(ctx.author.name, ctx.author.global_name)
            if rank_up_message:
                await ctx.channel.send(rank_up_message)

            # Send the coinflip result message
            await ctx.channel.send(cf_result)

        except Exception as e:
            print(e)
            await ctx.channel.send('Something went wrong, no idea what')

    @casino_coinflip.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'Calm the fuck down.')

    @commands.command(help="Play roulette! Bet on a number, color, or even/odd!")
    @commands.cooldown(1, 5, commands.BucketType.user)  # Cooldown to prevent spam
    async def roulette(self, ctx, bet_type: str, bet_value: str, bet_amount: str):
        botConsole.log_command(ctx)
        rank_up_message = await update_rank(ctx.author.name, ctx.author.global_name)
        if rank_up_message:
            await ctx.channel.send(rank_up_message)
        if 'k' in to_bet:
            to_bet = to_bet.replace('k', '000')
        await casino_roulette(ctx, bet_type, bet_value, bet_amount)

    @commands.command(
        name="diceroll",  # Name of the command
        help="Roll a dice and bet an amount to win!",  # Help description
        aliases=['dr', 'dice']  # Optional: Shorter aliases
    )
    @commands.cooldown(1, 5, commands.BucketType.user)  # 5-second cooldown
    async def dice_roll(self, ctx, amount: str):
        botConsole.log_command(ctx)
        # Call the dice roll function from casino.py
        rank_up_message = await update_rank(ctx.author.name, ctx.author.global_name)
        if rank_up_message:
            await ctx.channel.send(rank_up_message)

        if 'k' in amount:
            amount = amount.replace('k', '000')

        await casino_diceroll(ctx, amount)

    @commands.command(
        help='Receive some help from the casino',
        aliases=['gib']
    )
    async def casino_chip_gib(self, ctx):
        botConsole.log_command(ctx)
        gib_message = casino.casino_contribution(ctx)
        await ctx.channel.send(embed=gib_message)

    @casino_chip_gib.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(
                f'Casino is done giving you free chips. Ask again in {round(error.retry_after, 0)} seconds')

    @commands.command(
        aliases=['sjekkels', 'sj', 's']
    )
    async def check_chips(self, ctx):
        chip_balance = casino.check_user_chips(ctx)
        await ctx.channel.send(embed=chip_balance)

    @commands.command(
        aliases=['donate', 'give']
    )
    async def donate_chips(self, ctx, amount: str):
        botConsole.log_command(ctx)

        if not ctx.message.mentions:
            await ctx.channel.send('You must mention a user to donate to')
            return

        try:
            if 'k' in amount:
                amount = amount.replace('k', '000')
            await casino.donate(ctx, amount)
        except Exception as e:
            print(e)
            await ctx.channel.send('Something went wrong')


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
        # await bot.add_cog(Daddy(bot))
        await bot.add_cog(JeffThings(bot))
        await bot.add_cog(Casino(bot))
        await bot.add_cog(Fun(bot))
        await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
