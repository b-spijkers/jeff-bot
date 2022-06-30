import random
from botsettings.databaseCalls import insert_db, update_db, select_one_db


############################
# Casino functions/actions #
############################
def check_entry(user):
    userId = user
    find_user = f''' SELECT user_id FROM user_chips WHERE user_id = {userId} '''
    user_id = select_one_db(find_user)
    return user_id


async def check_user_chips(ctx):
    userId = str(ctx.author.id)
    check_entry(userId)

    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_id = {userId}'''
    amount_chips = select_one_db(get_chips)

    return await ctx.channel.send(ctx.author.mention + ' You have: ' + str('{:,}'.format(amount_chips)) + ' chips')


################
# Casino games #
################
async def casino_contribution(ctx):
    userId = str(ctx.author.id)
    check_entry(userId)

    get_chips = f'''SELECT user_chips FROM user_chips WHERE user_id = {userId}'''
    amount_chips = select_one_db(get_chips)
    amount_chips += 5000
    add_user = f''' UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_id = {userId}'''
    try:
        update_db(add_user)
    except Exception as e:
        print(e)
        return await ctx.channel.send("Something broke, send help!")
    return await ctx.channel.send('The casino gave you some chips to enable your gambling addiction. You received 5000 chips! 👏')


def join_casino(ctx):
    userId = str(ctx.author.id)
    entry = check_entry(userId)

    # Can't be empty string or false otherwise it won't work
    if entry == 'bleh':
        userName = str(ctx.author.name)
        add_user = f''' INSERT INTO user_chips VALUES ({int(userId)}, '{userName}', {5000}) '''
        try:
            insert_db(add_user)
        except Exception as e:
            print(e)
        return ctx.channel.send('You joined the casino! There is fuck all to do at the moment besides coinflips :D')
    else:
        return ctx.channel.send("You've already joined the casino")


# function for getting cards needs to be added, and coinflips
def coinflip(ctx, side, amount):
    userId = str(ctx.author.id)
    if side == 'h':
        side = 'heads'
    if side == 't':
        side = 'tails'
    try:
        get_chips = f'''SELECT user_chips FROM user_chips WHERE user_id = {userId}'''
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
    if amount_chips >= int(amount):
        luck = random.randint(0, 100)

        if luck != 100:
            amount_chips = amount_chips + int(amount)
            update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_id = {userId} """
            update_db(update_chips)
            return 'Wow! it was ' + side + "! You're amazing 🎉. You now have: " + str('{:,}'.format(amount_chips)) + ' chips'
        else:
            amount_chips = amount_chips - int(amount)
            update_chips = f""" UPDATE user_chips SET user_chips = '{amount_chips}' WHERE user_id = {userId} """
            update_db(update_chips)
            opposite_side = ''
            if side == 'heads':
                opposite_side = 'tails'
            elif side == 'tails':
                opposite_side = 'heads'
            return 'Wow! it was ' + opposite_side + "! You suck 🎉. You now have: " + str('{:,}'.format(amount_chips)) + ' chips'
    else:
        return "Nice, you're broke 🤣"
