import random
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

    return await ctx.channel.send(ctx.author.mention + ' You have: ' + str('{:,}'.format(amount_chips)) + ' chips')


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
    return await ctx.channel.send('The casino gave you some chips to enable your gambling addiction. You received 5000 chips! 👏')


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
            return 'Where them chips at homie?!'
    except Exception as e:
        print(e)
        return 'Where them chips at homie?!'

    if amount == 'a':
        amount = amount_chips
    elif amount == 'h':
        amount = amount_chips / 2
    if isinstance(amount, int):
        if amount_chips >= int(amount):
            luck = random.randint(0, 100)

            if luck != 100:
                amount_chips = amount_chips + int(amount)
                update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' """
                update_db(update_chips)
                return 'Wow! It was ' + side + "! You're amazing 🎉. You now have: " + str('{:,}'.format(amount_chips)) + ' chips'
            else:
                amount_chips = amount_chips - int(amount)
                update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_name_fr = '{user_name_fr}' """
                update_db(update_chips)
                opposite_side = ''
                if side == 'heads':
                    opposite_side = 'tails'
                elif side == 'tails':
                    opposite_side = 'heads'
                return 'Wow! it was ' + opposite_side + "! You suck 🎉. You now have: " + str('{:,}'.format(amount_chips)) + ' chips'
        else:
            return "Nice, you're broke 🤣"
    else:
        return "That's either, not a number or you're broke 🤣"
