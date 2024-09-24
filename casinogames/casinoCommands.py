import math
from datetime import datetime, timedelta
import random

import asyncio
import discord

from botsettings.databaseCalls import insert_db, update_db, select_one_db


############################
# Casino functions/actions #
############################
def check_entry(user):
    user_name = user
    find_user = f''' SELECT user_name_fr FROM user_chips WHERE user_name_fr = '{user_name}' '''
    user_name_fr = select_one_db(find_user)
    return user_name_fr


async def check_user_chips(ctx):
    user_name_fr = str(ctx.author.name)
    check_entry(user_name_fr)

    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    amount_chips = select_one_db(get_chips)

    return await ctx.channel.send(ctx.author.mention + ' You have: **' + str(
        '{:,}'.format(amount_chips)) + '** <:Shekel:1286655809098354749> **Sjekkels**')


def get_profile(ctx):
    user_name_fr = str(ctx.author.name)

    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_chips = select_one_db(get_chips)

    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    # Create an embed object
    embed = discord.Embed(
        title=f"{ctx.author.global_name}'s Profile",
        description=f"Stats",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="<:Shekel:1286655809098354749> Sjekkel Amount",
        value=f"**{user_chips:,}** <:Shekel:1286655809098354749> **Sjekkels**",
        inline=False
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

    embed.set_footer(text="Keep gambling and gain more **XP** to prestige!")
    return embed


def reward_user_with_chips(user_name_fr, amount):
    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_chips = select_one_db(get_chips)

    user_chips += amount
    update_chips = f'''UPDATE user_chips SET user_chips = {user_chips} WHERE user_name_fr = '{user_name_fr}' '''
    update_db(update_chips)


def prestige_user(user_name_fr):
    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    reset_xp = f'''UPDATE user_chips SET user_xp = 0, user_prestige = {user_prestige} WHERE user_name_fr = '{user_name_fr}' '''
    update_db(reset_xp)

    reward_chips = 10000 * user_prestige
    reward_user_with_chips(user_name_fr, reward_chips)


def add_xp(user_name_fr, xp_gain):
    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    user_xp += xp_gain

    update_xp = f'''UPDATE user_chips SET user_xp = {user_xp} WHERE user_name_fr = '{user_name_fr}' '''
    update_db(update_xp)


PRESTIGE_XP_CAP_BASE = 10000000  # Base XP cap for prestige


def calculate_prestige_xp_cap(user_prestige):
    """Calculate the XP required for prestige based on the user's current prestige level."""
    return math.ceil(PRESTIGE_XP_CAP_BASE * (user_prestige * 0.25 + 1))


async def prestige(ctx):
    user_name_fr = str(ctx.author.name)

    # Fetch user XP and prestige level from the database
    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    # Calculate XP required to prestige
    prestige_xp_cap = calculate_prestige_xp_cap(user_prestige)

    if user_xp >= prestige_xp_cap:
        # User is eligible to prestige
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

        # Send the embed and prompt for confirmation
        prestige_message = await ctx.send(embed=embed)
        await prestige_message.add_reaction('👍')
        await prestige_message.add_reaction('👎')

        # Check if the user reacts with thumbs-up or thumbs-down
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['👍',
                                                                  '👎'] and reaction.message.id == prestige_message.id

        try:
            # Wait for the user's reaction (60 seconds timeout)
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '👍':
                # User confirmed to prestige
                await apply_prestige(ctx, user_name_fr, new_prestige_level, reward_chips)
            else:
                # User canceled the prestige process
                await ctx.send(f"Bitch.")
        except asyncio.TimeoutError:
            # Handle timeout if the user doesn't react in time
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
    """Apply the prestige process, increase the prestige level, reset XP, and give rewards."""
    try:
        # Reset user XP and increase prestige level
        update_prestige = f'''UPDATE user_chips SET user_prestige = {new_prestige_level}, user_xp = 0 WHERE user_name_fr = '{user_name_fr}' '''
        update_db(update_prestige)

        # Give reward chips for prestige
        update_chips = f'''UPDATE user_chips SET user_chips = {reward_chips} WHERE user_name_fr = '{user_name_fr}' '''
        update_db(update_chips)

        # Notify the user of successful prestige
        await ctx.send(
            f"🎉 Congratulations {ctx.author.mention}! You have prestiged to **level {new_prestige_level}** and received **{reward_chips:,}** <:Shekel:1286655809098354749> **Sjekkels**!")
    except Exception as e:
        await ctx.send("Something went wrong with the prestige process.")
        print(e)


RANK_STEPS = [1000, 10000, 100000, 1000000, 10000000]


def calculate_rank_xp(user_prestige):
    return [math.ceil(rank_step * (user_prestige * 0.25 + 1)) for rank_step in RANK_STEPS]


async def update_rank(user_name_fr, user_name_global):
    get_user_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_user_xp)

    get_rank = f'''SELECT user_rank FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    current_rank = select_one_db(get_rank)

    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    required_xp = calculate_rank_xp(user_prestige)

    for i in range(current_rank, len(RANK_STEPS)):
        if user_xp >= required_xp[i]:
            # Rank up the user
            new_rank = i + 1
            update_rank_query = f'''UPDATE user_chips SET user_rank = {new_rank} WHERE user_name_fr = '{user_name_fr}' '''
            update_db(update_rank_query)

            return f"Congratulations {user_name_global}! You've ranked up to **Rank {new_rank}**!"

    return None  # No rank up


DAILY_REWARD_AMOUNT = 250  # Define the reward amount (customize as needed)

def daily_reward(ctx):
    user_name_fr = str(ctx.author.name)

    # Fetch the last time the user claimed the daily reward
    get_last_claim = f'''SELECT daily_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    last_claim = select_one_db(get_last_claim)

    # if last_claim == 'bleh':  # If user doesn't exist in the database
    #     return await ctx.send("You need to register first by joining the casino!")

    # Convert `last_claim` to a datetime object
    # last_claim_time = datetime.strptime(last_claim, '%Y-%m-%d %H:%M:%S')

    # Get the current time
    current_time = datetime.now()

    # Check if 24 hours (1 day) have passed since the last claim
    time_since_last_claim = current_time - last_claim
    if time_since_last_claim >= timedelta(days=1):
        print("Eligible")
        # Eligible for daily reward
        reward_chips = DAILY_REWARD_AMOUNT

        # Update the user's chips
        get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
        user_chips = select_one_db(get_chips)

        new_chip_amount = user_chips + reward_chips

        update_chips = f'''UPDATE user_chips SET user_chips = {new_chip_amount}, daily_chips = '{current_time}' WHERE user_name_fr = '{user_name_fr}' '''
        update_db(update_chips)

        # Send reward message
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
        print('Not eligible')
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


################
# Casino games #
################
async def casino_contribution(ctx):
    user_name_fr = str(ctx.author.name)
    check_entry(user_name_fr)

    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    amount_chips = select_one_db(get_chips)
    amount_chips += 5000
    add_user = f''' UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' '''
    try:
        update_db(add_user)
    except Exception as e:
        print(e)
        return await ctx.channel.send("Something broke, send help!")
    return await ctx.channel.send(
        'The casino gave you some chips to enable your gambling addiction. You received **5000** <:Shekel:1286655809098354749> **Sjekkels**! 👏')


def join_casino(ctx):
    user_name_fr = str(ctx.author.name)
    entry = check_entry(user_name_fr)

    # Can't be empty string or false otherwise it won't work
    if entry == 'bleh':
        userName_global = str(ctx.author.global_name)
        add_user = f''' INSERT INTO user_chips VALUES ('{user_name_fr}', '{userName_global}', {5000}) '''
        try:
            insert_db(add_user)
        except Exception as e:
            print(e)
        return ctx.channel.send('You joined the casino! There is fuck all to do at the moment besides coinflips :D')
    else:
        return ctx.channel.send("You've already joined the casino")


def is_round_number(num):
    return num % 1 == 0


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
        get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
        amount_chips = select_one_db(get_chips)
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
                print(int(amount_chips))
                print(int(amount))
                amount_chips = int(amount_chips) + int(amount)
                update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' """
                update_db(update_chips)
                xp_earned = amount
                add_xp(user_name_fr, xp_earned)

                return 'Wow! It was ' + side + "! You **won** 🎉. You now have: " + str(
                    '{:,}'.format(amount_chips)) + ' <:Shekel:1286655809098354749> **Sjekkels**. And earned: **' + str(
                    xp_earned) + 'XP**!'
            else:
                amount_chips = int(amount_chips) - int(amount)
                update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' """
                update_db(update_chips)
                opposite_side = 'tails' if side == 'heads' else 'heads'
                return 'Wow! it was ' + opposite_side + "! You **lost** <:theman:1286723740880732210>. You now have: **" + str(
                    '{:,}'.format(amount_chips)) + '** <:Shekel:1286655809098354749> **Sjekkels**.'
        else:
            return "Nice, you're broke 🤣"
    else:
        return "That's either, not a number or you're broke 🤣"


def send_rank_info(ctx):
    user_name_fr = str(ctx.author.name)
    user_name_global = str(ctx.author.global_name)

    check_entry(user_name_fr)
    """Send an embed showing the user's rank and XP required for the next rank."""

    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    get_rank = f'''SELECT user_rank FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    current_rank = select_one_db(get_rank)

    required_xp = calculate_rank_xp(user_prestige)

    embed = discord.Embed(title=f"{user_name_global}'s Rank Information", color=discord.Color.blue())
    embed.add_field(name="Current XP", value=f"**{user_xp:,}**", inline=False)
    embed.add_field(name="Current Rank", value=f"**Rank {current_rank}**", inline=False)



    for i, xp in enumerate(required_xp, start=1):
        status = "Reached" if current_rank >= i else "Next"
        embed.add_field(name= f"Rank {i} (**Unlocks Prestige**)" if i == 5 else f"Rank {i}", value=f"**{xp:,} XP** (**{status}**)", inline=False)

    return embed
