import random

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

    return await ctx.channel.send(ctx.author.mention + ' You have: ' + str('{:,}'.format(amount_chips)) + ' Sjekkels')


def get_profile(ctx):
    user_name_fr = str(ctx.author.name)

    # Fetch the user's chip amount
    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_chips = select_one_db(get_chips)

    # Fetch the user's total XP
    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    # Fetch the user's prestige level (assuming it's stored in the database)
    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    # Create an embed object
    embed = discord.Embed(
        title=f"{ctx.author.global_name}'s Profile",  # Embed title showing the user's name
        description=f"Here is your current casino profile, {ctx.author.mention}!",  # Brief description
        color=discord.Color.blue()  # Set embed color (can be customized)
    )

    # Add chip count as a field in the embed
    embed.add_field(
        name="💰 Chip Amount",  # Field title
        value=f"{user_chips:,} Sjekkels",  # Display formatted chip amount
        inline=False  # Ensures it takes the full width
    )

    # Add XP total as a field in the embed
    embed.add_field(
        name="🏅 Total XP",  # Field title
        value=f"{user_xp:,} XP",  # Display formatted XP amount
        inline=True  # Set inline to True for side-by-side display
    )

    # Add prestige level as a field in the embed
    embed.add_field(
        name="🌟 Prestige Level",  # Field title
        value=f"Level {user_prestige}",  # Display the user's prestige level
        inline=True  # Set inline to True to align next to the XP
    )

    # Optionally, you can add a footer or thumbnail for a richer embed message
    embed.set_footer(text="Keep gambling and gain more XP to prestige!")  # Add a footer note

    # Send the embed message in the channel
    return embed


def reward_user_with_chips(user_name_fr, amount):
    # Fetch current chips
    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_chips = select_one_db(get_chips)

    # Add chips to user
    user_chips += amount
    update_chips = f'''UPDATE user_chips SET user_chips = {user_chips} WHERE user_name_fr = '{user_name_fr}' '''
    update_db(update_chips)


def prestige_user(user_name_fr):
    # Increase prestige level (assuming there's a prestige column in the database)
    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    # Reset XP to 0 after prestiging
    reset_xp = f'''UPDATE user_chips SET user_xp = 0, user_prestige = {user_prestige} WHERE user_name_fr = '{user_name_fr}' '''
    update_db(reset_xp)

    # Reward the user for prestiging
    reward_chips = 10000 * user_prestige  # Example reward scaling with prestige
    reward_user_with_chips(user_name_fr, reward_chips)


def add_xp(user_name_fr, xp_gain):
    # Fetch current XP
    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    # Add XP
    user_xp += xp_gain

    # Update XP in database
    update_xp = f'''UPDATE user_chips SET user_xp = {user_xp} WHERE user_name_fr = '{user_name_fr}' '''
    update_db(update_xp)

    # Check if the user is eligible for prestige
    if user_xp >= 10000:  # Example threshold for prestige
        prestige_user(user_name_fr)


def prestige(ctx):
    user_name_fr = str(ctx.author.name)

    # Fetch the user's current XP and Prestige Level
    get_xp = f'''SELECT user_xp FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_xp = select_one_db(get_xp)

    get_prestige = f'''SELECT user_prestige FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
    user_prestige = select_one_db(get_prestige)

    # Calculate the XP cap for the next prestige
    prestige_xp_cap = 100000 * (user_prestige * 2)

    # Check if the user has enough XP to prestige
    if user_xp >= prestige_xp_cap:
        # User can prestige, so we upgrade their prestige level
        new_prestige_level = user_prestige + 1

        # Update the user's prestige level and reset XP
        update_prestige = f'''UPDATE user_chips SET user_prestige = {new_prestige_level}, user_xp = 0 WHERE user_name_fr = '{user_name_fr}' '''
        update_db(update_prestige)

        # Reward the user with more chips upon prestiging
        reward_chips = 5000 * new_prestige_level  # For example, reward increases by prestige level
        get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
        user_chips = select_one_db(get_chips)

        new_chip_amount = user_chips + reward_chips
        update_chips = f'''UPDATE user_chips SET user_chips = {new_chip_amount} WHERE user_name_fr = '{user_name_fr}' '''
        update_db(update_chips)

        # Create a success embed to let the user know they've prestiged
        embed = discord.Embed(
            title="🌟 Prestige Successful!",
            description=f"Congratulations {ctx.author.mention}! You've prestiged to **Level {new_prestige_level}**.",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="💰 Chip Reward",
            value=f"You've received {reward_chips:,} Sjekkels as a reward for prestiging!",
            inline=False
        )
        embed.add_field(
            name="🏅 XP Reset",
            value=f"Your XP has been reset",
            inline=False
        )
        embed.set_footer(text="Keep gambling to reach the next prestige!")

        # Send the embed message
        return embed
    else:
        # User doesn't have enough XP to prestige yet
        embed = discord.Embed(
            title="🌟 Prestige Not Yet Available",
            description=f"You need more XP to prestige, {ctx.author.mention}.",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🏅 Current XP",
            value=f"{user_xp:,} XP",
            inline=True
        )
        embed.add_field(
            name="🚀 XP Needed",
            value=f"{prestige_xp_cap - user_xp:,} more XP needed to prestige.",
            inline=True
        )
        embed.set_footer(text="Keep gambling to gain more XP!")

        # Send the embed message
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
        'The casino gave you some chips to enable your gambling addiction. You received 5000 Sjekkels! 👏')


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


# function for getting cards needs to be added, and coinflips
def coinflip(ctx, side, amount):
    user_name_fr = str(ctx.author.name)

    print('Amount: ' + amount)
    print('Side: ' + side)

    if side == 'h' or side == 'heads':
        side = 'heads'
    elif side == 't' or side == 'tails':
        side = 'tails'
    else:
        return "First heads(h)/tails(t) then the amount..."
    try:
        get_chips = f'''SELECT user_chips FROM user_chips WHERE user_name_fr = '{user_name_fr}' '''
        amount_chips = select_one_db(get_chips)
        if amount_chips == 0:
            return 'Where them Sjekkels at homie?!'
    except Exception as e:
        print(e)
        return 'Where them Sjekkels at homie?!'

    if amount == 'a':
        amount = amount_chips
    elif amount == 'h':
        amount = amount_chips / 2

    amount = int(amount)

    if isinstance(amount, int):
        if amount_chips >= int(amount):
            luck = random.randint(0, 100)

            if luck >= 50:
                amount_chips += int(amount)
                update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' """
                update_db(update_chips)
                xp_earned = amount
                add_xp(user_name_fr, xp_earned)
                return 'Wow! It was ' + side + "! You're amazing 🎉. You now have: " + str(
                    '{:,}'.format(amount_chips)) + ' Sjekkels. And earned: ' + str(xp_earned) + 'XP!'
            else:
                amount_chips -= int(amount)
                update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' """
                update_db(update_chips)
                opposite_side = 'tails' if side == 'heads' else 'heads'
                return 'Wow! it was ' + opposite_side + "! You suck. You now have: " + str(
                    '{:,}'.format(amount_chips)) + ' Sjekkels.'
        else:
            return "Nice, you're broke 🤣"
    else:
        return "That's either, not a number or you're broke 🤣"
