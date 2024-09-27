import math
import secrets
from datetime import datetime, timedelta
import random
import asyncio
import discord

from botsettings.databaseCalls import insert_db, update_db, select_one_db

#######################################
# Casino Getter and Setter Functions. #
#######################################

# Reward Base values
CASINO_GIFT_AMOUNT = 1500
GIB_REWARD_AMOUNT = secrets.randbelow(125) + 25
HOURLY_REWARD_AMOUNT = 100
DAILY_REWARD_AMOUNT = 250
MONTHLY_REWARD_AMOUNT = 1000

# Rank and Prestige XP Base
PRESTIGE_XP_CAP_BASE = 10000000  # Base XP cap for prestige
RANK_STEPS = [1000, 10000, 100000, 1000000, 10000000]

# Constants for dice roll
XP_MULTIPLIER = 1  # Example multiplier for XP
WIN_MULTIPLIER = 5  # The multiplier for the winning amount on a 6 roll
PRESTIGE_MULTIPLIER = 0.25
RANK_MULTIPLIER = 1

def calculate_rank_xp(user_prestige, user_rank):
    return [math.ceil(rank_step * (user_prestige * PRESTIGE_MULTIPLIER + 1)) for rank_step in RANK_STEPS]

def calculate_prestige_xp_cap(user_prestige, user_rank):
    return math.ceil(PRESTIGE_XP_CAP_BASE * (user_prestige * PRESTIGE_MULTIPLIER + 1))

#TODO: Get this to work so you can't use decimal amount of chips to bet
def is_round_number(num):
    return num % 1 == 0

def get_chips(user_name):
    user_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name}' '''

    chips = select_one_db(user_chips)

    return chips

def add_new_user(user_name, nickname):
    datetime_minus_one = datetime.now() - timedelta(days=1)
    add_user = f''' INSERT INTO user_chips VALUES ('{user_name}', '{nickname}', {CASINO_GIFT_AMOUNT}, 0, 0, '{datetime_minus_one}', '{datetime_minus_one}') '''
    update_db(add_user)

def get_xp(user_name):
    user_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name}' '''

    xp = select_one_db(user_xp)

    return xp

def get_prestige(user_name):
    user_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name}' '''

    prestige = select_one_db(user_prestige)

    return prestige

def get_rank(user_name):
    user_rank = f'''SELECT user_rank FROM user_chips WHERE user_name_fr = '{user_name}' '''

    rank = select_one_db(user_rank)

    return rank

def get_hourly_date(user_name):
    get_user_hourly_date = f'''SELECT hourly_time FROM user_chips WHERE user_name_fr = '{user_name}' '''

    hourly_date = select_one_db(get_user_hourly_date)

    return hourly_date

def get_daily_date(user_name):
    get_user_daily_date = f'''SELECT daily_chips FROM user_chips WHERE user_name_fr = '{user_name}' '''

    daily_date = select_one_db(get_user_daily_date)

    return daily_date

def get_monthly_date(user_name):
    get_user_monthly_date = f'''SELECT monthly_chips FROM user_chips WHERE user_name_fr = '{user_name}' '''

    monthly_date = select_one_db(get_user_monthly_date)

    return monthly_date

def get_gib_time(user_name):
    get_user_gib_date = f'''SELECT gib_time FROM user_chips WHERE user_name_fr = '{user_name}' '''

    gib_time = select_one_db(get_user_gib_date)

    return gib_time

def update_user_chips(user_name, chips):
    update_chips = f'''UPDATE user_chips SET user_chips = {chips} WHERE user_name_fr = '{user_name}' '''
    update_db(update_chips)

def update_gib_time(user_name, gib_time):
    update_gib_date = f'''UPDATE user_chips SET gib_time = '{gib_time}' WHERE user_name_fr = '{user_name}' '''
    update_db(update_gib_date)

def update_user_chips_hourly(user_name, chips, current_datetime):
    update_chips_hourly = f'''UPDATE user_chips SET user_chips = {chips}, hourly_time = '{current_datetime}' WHERE user_name_fr = '{user_name}' '''
    update_db(update_chips_hourly)

def update_user_chips_daily(user_name, chips, current_datetime):
    update_chips_daily = f'''UPDATE user_chips SET user_chips = {chips}, daily_chips = '{current_datetime}' WHERE user_name_fr = '{user_name}' '''
    update_db(update_chips_daily)

def update_user_chips_monthly(user_name, chips, current_datetime):
    update_chips_monthly = f'''UPDATE user_chips SET user_chips = {chips}, monthly_chips = '{current_datetime}' WHERE user_name_fr = '{user_name}' '''
    update_db(update_chips_monthly)

def update_user_xp(user_name, xp):
    update_xp = f'''UPDATE user_chips SET user_xp = {xp} WHERE user_name_fr = '{user_name}' '''
    update_db(update_xp)

def update_user_prestige(user_name, prestige):
    update_prestige = f'''UPDATE user_chips SET user_prestige = {prestige}, user_xp = 0 WHERE user_name_fr = '{user_name}' '''
    update_db(update_prestige)

def update_user_rank(user_name, rank):
    update_rank = f'''UPDATE user_cgips SET user_rank = {rank} WHERE user_name_fr = '{user_name}' '''
    update_db(update_rank)

def reset_xp(user_name, prestige):
    reset_xp = f'''UPDATE user_chips SET user_xp = 0, user_prestige = {prestige} WHERE user_name_fr = '{user_name}' '''
    update_db(reset_xp)

def add_xp(user_name_fr, xp_gain):
    user_xp = get_xp(user_name_fr)
    user_xp += xp_gain

    update_user_xp(user_name_fr, user_xp)

####################################
# Casino profile functions/actions #
####################################

def join_casino(ctx):
    user_name_fr = str(ctx.author.name)
    entry = check_entry(user_name_fr)

    # Can't be empty string or false otherwise it won't work
    if entry == 'bleh':
        userName_global = str(ctx.author.global_name)
        try:
            add_new_user(user_name_fr, userName_global)
        except Exception as e:
            print(e)
        return ctx.channel.send('You joined the casino! There is fuck all to do at the moment besides coinflips :D')
    else:
        return ctx.channel.send("You've already joined the casino")


def check_entry(user):
    user_name = user
    find_user = f''' SELECT user_name_fr FROM user_chips WHERE user_name_fr = '{user_name}' '''
    user_name_fr = select_one_db(find_user)
    return user_name_fr


def check_user_chips(ctx):
    user_name_fr = str(ctx.author.name)

    # Check if the user is in the database
    check_entry(user_name_fr)

    # Retrieve the user's chip amount
    amount_chips = get_chips(user_name_fr)

    # Create an embed message to display the user's chip balance
    embed = discord.Embed(
        title="<:Shekel:1286655809098354749> Sjekkel Balance",
        color=discord.Color.blue()
    )

    # Add a field to show the number of chips in a formatted manner
    embed.add_field(
        name=f"**{amount_chips:,}** <:Shekel:1286655809098354749> **Sjekkels**",
        value='',
        inline=False
    )

    # Add a footer for extra context
    embed.set_footer(text="Wow! I have way more than that. Loser!")

    # Send the embed message to the channel
    return embed


def get_profile(ctx):
    user_name_fr = str(ctx.author.name)

    user_chips = get_chips(user_name_fr)
    user_xp = get_xp(user_name_fr)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)

    # Create an embed object
    embed = discord.Embed(
        title=f"{ctx.author.global_name}'s Profile",
        description=f"Stats",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🎖️ Rank",
        value=f"Rank **{user_rank:,}**",
        inline=True
    )

    embed.add_field(
        name="🏅 Total XP",
        value=f"**{user_xp:,} XP**",
        inline=True
    )

    embed.add_field(
        name="🌟 Prestige Level",
        value=f"Level {user_prestige}",
        inline=True
    )

    embed.add_field(
        name="<:Shekel:1286655809098354749> Sjekkel Amount",
        value=f"**{user_chips:,}** <:Shekel:1286655809098354749> **Sjekkels**",
        inline=False
    )

    embed.set_footer(text="Keep gambling and gain more **XP** to prestige! And most of all to give me more money!")
    return embed


async def prestige(ctx):
    user_name_fr = str(ctx.author.name)

    user_xp = get_xp(user_name_fr)

    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)

    # Calculate XP required to prestige
    prestige_xp_cap = calculate_prestige_xp_cap(user_prestige, user_rank)

    if user_xp >= prestige_xp_cap:
        new_prestige_level = user_prestige + 1
        reward_chips = 500 * new_prestige_level  # Example: Rewards scale with prestige level

        embed = discord.Embed(
            title="🌟 Prestige Available!",
            description=f"Good shit {ctx.author.mention}! You can prestige to **Level {new_prestige_level}**.",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="<:Shekel:1286655809098354749> Sjekkel Reward",
            value=f"You will receive **{reward_chips:,}** <:Shekel:1286655809098354749> **Sjekkels** as a reward upon prestiging. Which you'll lose in no time.",
            inline=False
        )
        embed.add_field(
            name="🏅 XP and Sjekkels Reset",
            value="Your **XP** and <:Shekel:1286655809098354749> **Sjekkels** will be reset to 0.",
            inline=False
        )
        embed.set_footer(text="React with 👍 to prestige, or 👎 to cancel.")

        prestige_message = await ctx.send(embed=embed)

        await prestige_message.add_reaction('👍')
        await prestige_message.add_reaction('👎')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['👍',
                                                                  '👎'] and reaction.message.id == prestige_message.id

        try:
            # Wait for the user's reaction (60 seconds timeout)
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '👍':
                await apply_prestige(ctx, user_name_fr, new_prestige_level, reward_chips)
            else:
                await ctx.send(f"Bitch.")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention}, hurry up next time!. Fucking hell.")
    else:
        # User is not eligible to prestige
        embed = discord.Embed(
            title="🌟 Prestige Not Yet Available",
            description=f"You need more XP to prestige, {ctx.author.mention}.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🏅 Current XP",
            value=f"**{user_xp:,} XP**",
            inline=True
        )
        embed.add_field(
            name="🚀 XP Needed",
            value=f"**{prestige_xp_cap - user_xp:,}** more **XP** needed to prestige.",
            inline=True
        )
        embed.set_footer(text="Keep gambling to gain more XP!")

        await ctx.send(embed=embed)


async def apply_prestige(ctx, user_name_fr, new_prestige_level, reward_chips):
    try:
        update_user_prestige(user_name_fr, new_prestige_level)
        update_user_chips(user_name_fr, reward_chips)

        await ctx.send(
            f"🎉 Congratulations {ctx.author.mention}! You have prestiged to **level {new_prestige_level}** and received **{reward_chips:,}** <:Shekel:1286655809098354749> **Sjekkels**!")
    except Exception as e:
        await ctx.send("Something went wrong with the prestige process.")
        print(e)

def send_rank_info(ctx):
    user_name_fr = str(ctx.author.name)
    user_name_global = str(ctx.author.global_name)

    check_entry(user_name_fr)

    user_xp = get_xp(user_name_fr)
    user_prestige = get_prestige(user_name_fr)
    current_rank = get_rank(user_name_fr)

    required_xp = calculate_rank_xp(user_prestige, current_rank)

    embed = discord.Embed(title=f"{user_name_global}'s Rank Information", color=discord.Color.blue())
    embed.add_field(name="Current XP", value=f"**{user_xp:,}**", inline=False)
    embed.add_field(name="Current Rank", value=f"**Rank {current_rank}**", inline=False)



    for i, xp in enumerate(required_xp, start=1):
        status = "Reached" if current_rank >= i else "Next"
        embed.add_field(name= f"Rank {i} (**Unlocks Prestige**)" if i == 5 else f"Rank {i}", value=f"**{xp:,} XP** (**{status}**)", inline=False)

    return embed


async def update_rank(user_name_fr, user_name_global):
    user_xp = get_xp(user_name_fr)
    current_rank = get_rank(user_name_fr)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)

    required_xp = calculate_rank_xp(user_prestige, user_rank)

    for i in range(current_rank, len(RANK_STEPS)):
        if user_xp >= required_xp[i]:

            new_rank = i + 1
            update_user_rank(user_name_global, new_rank)

            return f"{user_name_global}. You've ranked up to **Rank {new_rank}**. Don't get too excited"

    return None  # No rank up

def hourly_reward(ctx):
    user_name_fr = str(ctx.author.name)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)
    last_claim = get_hourly_date(user_name_fr)

    current_time_stamp = datetime.now()

    time_since_last_claim = current_time_stamp - last_claim
    if time_since_last_claim >= timedelta(hours=1):

        reward_chips = math.ceil(HOURLY_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))
        user_chips = get_chips(user_name_fr)
        new_chip_amount = user_chips + reward_chips
        update_user_chips_hourly(user_name_fr, new_chip_amount, current_time_stamp)

        embed = discord.Embed(
            title="🎉 Hourly Reward Claimed!",
            description=f"{ctx.author.mention}, you have received **{reward_chips}** <:Shekel:1286655809098354749> Sjekkels! Go out and lose it all!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Current **Sjekkels**",
            value=f"**{new_chip_amount:,}** <:Shekel:1286655809098354749> **Sjekkels**",
            inline=True
        )
        embed.set_footer(text="Now fuck off")
        return embed
    else:
        # Not yet eligible for daily reward
        time_left = timedelta(hours=1) - time_since_last_claim
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        embed = discord.Embed(
            title="⏳ Nope. An hour hasn't passed since last time. Dumbass.",
            description=f"{ctx.author.mention}, you have already claimed your hourly <:Shekel:1286655809098354749> **Sjekkels**.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Time Remaining",
            value=f"You can claim again in {minutes} minutes.",
            inline=False
        )
        embed.set_footer(text="Come back when the timer expires! Shithead!")

        return embed


def daily_reward(ctx):
    user_name_fr = str(ctx.author.name)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)
    last_claim = get_daily_date(user_name_fr)

    current_time_stamp = datetime.now()

    time_since_last_claim = current_time_stamp - last_claim
    if time_since_last_claim >= timedelta(days=1):

        reward_chips = math.ceil(DAILY_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))
        user_chips = get_chips(user_name_fr)
        new_chip_amount = user_chips + reward_chips
        update_user_chips_daily(user_name_fr, new_chip_amount, current_time_stamp)

        embed = discord.Embed(
            title="🎉 Daily Reward Claimed!",
            description=f"{ctx.author.mention}, you have received **{reward_chips}** <:Shekel:1286655809098354749> Sjekkels! Go out and lose it all!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Current **Sjekkels**",
            value=f"**{new_chip_amount:,}** <:Shekel:1286655809098354749> **Sjekkels**",
            inline=True
        )
        embed.set_footer(text="Now fuck off")
        return embed
    else:
        # Not yet eligible for daily reward
        time_left = timedelta(days=1) - time_since_last_claim
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        embed = discord.Embed(
            title="⏳ It's called daily for reason, just wait 24 hours. Dumbass.",
            description=f"{ctx.author.mention}, you have already claimed your daily <:Shekel:1286655809098354749> **Sjekkels** today.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Time Remaining",
            value=f"You can claim again in {time_left.days} days, {hours} hours, and {minutes} minutes.",
            inline=False
        )
        embed.set_footer(text="Come back when the timer expires! Shithead!")

        return embed


def monthly_reward(ctx):
    user_name_fr = str(ctx.author.name)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)
    last_claim = get_monthly_date(user_name_fr)

    current_time_stamp = datetime.now()

    time_since_last_claim = current_time_stamp - last_claim

    if time_since_last_claim >= timedelta(days=30):
        reward_chips = math.ceil(MONTHLY_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))
        user_chips = get_chips(user_name_fr)
        new_chip_amount = user_chips + reward_chips

        update_user_chips_monthly(user_name_fr, new_chip_amount, current_time_stamp)

        embed = discord.Embed(
            title="🎉 Monthly Reward Claimed!",
            description=f"{ctx.author.mention}, you have received **{reward_chips}** <:Shekel:1286655809098354749> Sjekkels! Go out and lose it all!",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Current **Sjekkels**",
            value=f"**{new_chip_amount:,}** <:Shekel:1286655809098354749> **Sjekkels**",
            inline=True
        )
        embed.set_footer(text="Now fuck off")
        return embed
    else:
        # Not yet eligible for monthly reward
        time_left = timedelta(days=30) - time_since_last_claim
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        embed = discord.Embed(
            title="⏳Better luck, tomorrow or something",
            description=f"{ctx.author.mention}, you have already claimed your monthly <:Shekel:1286655809098354749> **Sjekkels**.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="Time Remaining",
            value=f"You can claim again in {days} days, {hours} hours, and {minutes} minutes.",
            inline=False
        )
        embed.set_footer(text="Come back when the timer expires! Shithead!")

        return embed


def combined_rewards(ctx):
    # Get the user's name
    user_name_fr = str(ctx.author.name)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)

    hourly_result = hourly_reward(ctx)
    gib_result = casino_contribution(ctx)

    # Call the daily reward function
    daily_result = daily_reward(ctx)

    # Call the monthly reward function
    monthly_result = monthly_reward(ctx)

    # Create the embed for combined rewards
    embed = discord.Embed(
        title="<:Shekel:1286655809098354749> Rewards Status",
        description=f"{ctx.author.mention}, here's your reward status for today:",
        color=discord.Color.blue()
    )

    if "Casino Charity Claimed!" in gib_result.title:
        embed.add_field(
            name="<:Shekel:1286655809098354749> Gib Reward",
            value=f"Successfully claimed **{math.ceil(GIB_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))}** <:Shekel:1286655809098354749> Sjekkels.",
            inline=False
        )
    else:
        embed.add_field(
            name="❌ Gib Reward",
            value=f"Already claimed. {gib_result.fields[0].value}",
            inline=False
        )

    if "Hourly Reward Claimed!" in hourly_result.title:
        embed.add_field(
            name="⏳ Hourly Reward",
            value=f"Successfully claimed **{math.ceil(HOURLY_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))}** <:Shekel:1286655809098354749> Sjekkels.",
            inline=False
        )
    else:
        embed.add_field(
            name="❌ Hourly Reward",
            value=f"Already claimed. {hourly_result.fields[0].value}",
            inline=False
        )

    if "Daily Reward Claimed!" in daily_result.title:
        embed.add_field(
            name="🎁 Daily Reward",
            value=f"Successfully claimed **{math.ceil(DAILY_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))}** <:Shekel:1286655809098354749> Sjekkels.",
            inline=False
        )
    else:
        embed.add_field(
            name="❌ Daily Reward",
            value=f"Already claimed. {daily_result.fields[0].value}",
            inline=False
        )

    if "Monthly Reward Claimed!" in monthly_result.title:
        embed.add_field(
            name="📅 Monthly Reward",
            value=f"Successfully claimed **{math.ceil(MONTHLY_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))}** <:Shekel:1286655809098354749> Sjekkels.",
            inline=False
        )
    else:
        embed.add_field(
            name="❌ Monthly Reward",
            value=f"Already claimed. {monthly_result.fields[0].value}",
            inline=False
        )

    # Return the embed message
    return embed

################
# Casino games #
################
def casino_contribution(ctx):
    user_name_fr = str(ctx.author.name)
    user_prestige = get_prestige(user_name_fr)
    user_rank = get_rank(user_name_fr)
    
    check_entry(user_name_fr)

    # Get current time
    current_time = datetime.now()

    # Get the last claim time (gib_time) from the database
    gib_time = get_gib_time(user_name_fr)  # You should have a function to retrieve gib_time from the database

    # Calculate time difference
    time_since_last_claim = current_time - gib_time

    # Check if 10 minutes have passed
    if time_since_last_claim < timedelta(minutes=5):
        # Time hasn't passed yet
        time_left = timedelta(minutes=5) - time_since_last_claim
        minutes, seconds = divmod(time_left.seconds, 60)

        embed = discord.Embed(
            title="⏳ Hold the fuck on!",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Time Remaining",
            value=f"You can claim again in {minutes} minute(s) and {seconds} second(s)",
            inline=False
        )
        return embed

    # 10 minutes have passed, give reward
    amount_chips = get_chips(user_name_fr)
    reward = math.ceil(GIB_REWARD_AMOUNT * (user_prestige * PRESTIGE_MULTIPLIER + 1 + user_rank * RANK_MULTIPLIER))
    amount_chips += reward

    update_user_chips(user_name_fr, amount_chips)
    update_gib_time(user_name_fr, current_time)

    # Create an embed message for a successful reward claim
    embed = discord.Embed(
        title="🎲 Casino Charity Claimed!",
        description=f"Take you <:Shekel:1286655809098354749> **Sjekkels** and fuck off!. You received **{reward}** <:Shekel:1286655809098354749> **Sjekkels**! 👏",
        color=discord.Color.green()
    )

    # Add fields to display additional info
    embed.add_field(
        name="Current Balance",
        value=f"You now have **{amount_chips:,}** <:Shekel:1286655809098354749> **Sjekkels**!",
        inline=False
    )

    embed.set_footer(text="It's only because of some legal bullshit you got this...")

    return embed


# function for getting cards needs to be added, and coinflips
def coinflip(ctx, side, amount):
    user_name_fr = str(ctx.author.name)

    if side == 'h' or side == 'heads':
        side = 'heads'
    elif side == 't' or side == 'tails':
        side = 'tails'
    else:
        return "First heads(h)/tails(t) then the <:Shekel:1286655809098354749> amount..."
    try:
        amount_chips = get_chips(user_name_fr)
        if amount_chips == 0:
            return 'Where them <:Shekel:1286655809098354749> **Sjekkels** at homie?!'
    except Exception as e:
        print(e)
        return 'Where them <:Shekel:1286655809098354749> **Sjekkels** at homie?!'

    if amount == 'a':
        amount = amount_chips
    elif amount == 'h':
        amount = amount_chips / 2
    else:
        amount = amount

    amount = int(amount)

    if isinstance(amount, int):
        if amount_chips >= int(amount):
            luck = random.randint(0, 100)

            if luck >= 50:
                amount_chips = int(amount_chips) + int(amount)
                update_user_chips(user_name_fr, amount_chips)
                xp_earned = amount
                add_xp(user_name_fr, xp_earned)

                return 'Wow! It was ' + side + "! You **won** 🎉. You now have: " + str(
                    '{:,}'.format(amount_chips)) + ' <:Shekel:1286655809098354749> **Sjekkels**. And earned: **' + str(
                    xp_earned) + 'XP**!'
            else:
                amount_chips = int(amount_chips) - int(amount)
                update_user_chips(user_name_fr, amount_chips)
                opposite_side = 'tails' if side == 'heads' else 'heads'
                return 'Wow! it was ' + opposite_side + "! You **lost** <:theman:1286723740880732210>. You now have: **" + str(
                    '{:,}'.format(amount_chips)) + '** <:Shekel:1286655809098354749> **Sjekkels**.'
        else:
            return "Nice, you're broke 🤣"
    else:
        return "That's either, not a number or you're broke 🤣"


#########################################
############# Dice Roll Game#############
#########################################

async def casino_diceroll(ctx, amount: int):
    user_name_fr = str(ctx.author.name)

    # Check if user is registered
    try:
        check_entry(user_name_fr)
    except Exception as e:
        print(e)
        return await ctx.send('First you must register yourself. Use <prefix>jc')

    # Fetch user chips
    user_chips = get_chips(user_name_fr)

    if user_chips < amount:
        return await ctx.send(f"You don't have enough chips to bet that amount, {ctx.author.mention}.")

    # Step 2: Show the "good luck" message with a spinning thumbnail
    embed = discord.Embed(
        title="<a:spin:1288783602636685394> Rolling the Dice... <a:spin:1288783602636685394>",
        description=f"<:theman:1286723740880732210> What will it be... <:theman:1286723740880732210>",
        color=discord.Color.blue()
    )
    initial_message = await ctx.send(embed=embed)

    # Step 3: Wait 3 seconds (using asyncio.sleep)
    await asyncio.sleep(3)

    # Roll the dice (random number between 1 and 6)
    dice_roll = secrets.randbelow(6) + 1

    # Step 4: Check if the result is 6
    if dice_roll == 6:
        reward = amount * WIN_MULTIPLIER
        new_chip_amount = user_chips + reward
        update_user_chips(user_name_fr, new_chip_amount)

        # Add XP based on the reward
        xp_earned = reward * XP_MULTIPLIER
        update_user_xp(user_name_fr, xp_earned)

        # Step 4: Edit the initial message to show the dice result (win)
        embed = discord.Embed(
            title="🎉 You rolled a 6!",
            description=f"Yippie.. {ctx.author.mention}, you rolled a 6 and won {reward:,} <:Shekel:1286655809098354749> **Sjekkels**",
            color=discord.Color.green()
        )
        embed.add_field(name="<:Shekel:1286655809098354749> Total Sjekkels", value=f"{new_chip_amount:,} <:Shekel:1286655809098354749> **Sjekkels**", inline=True)
        embed.add_field(name="🏅 XP Earned", value=f"{xp_earned:,} XP", inline=True)
        embed.set_footer(text="You'll lose the next one, don't worry...")
        await initial_message.edit(embed=embed)

    else:
        # Player loses the bet, subtract chips
        new_chip_amount = user_chips - amount
        update_user_chips(user_name_fr, new_chip_amount)

        # Step 4: Edit the initial message to show the dice result (loss)
        embed = discord.Embed(
            title=f"🎲 You rolled a {dice_roll}",
            description=f"Unlucky, {ctx.author.mention}. You rolled a {dice_roll} and lost {amount:,} <:Shekel:1286655809098354749> **Sjekkels**.",
            color=discord.Color.red()
        )
        embed.add_field(name="<:Shekel:1286655809098354749> Total Sjekkels", value=f"{new_chip_amount:,} <:Shekel:1286655809098354749> **Sjekkels**", inline=True)
        embed.set_footer(text="Loser")
        await initial_message.edit(embed=embed)
