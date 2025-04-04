import discord


async def jeff_info(self, ctx, bot):
    msg = discord.Embed(
        title='Jeff-bot info [current version: 3.1]',
        description="Currently Jeff uses 7 APIs to give you the best of random garbage. 1 of the APIs is kaput. "
                    "Use `<prefix>why` to figure out why",
        color=discord.Color.blurple()
    )

    msg.set_footer(
        text='Created by: BaronVonBarron#7882'
    )
    msg.set_author(
        name=bot.user.display_name,
        icon_url=bot.user.avatar
    )

    return await ctx.channel.send(embed=msg)


async def help(self, ctx, bot):
    msg = discord.Embed(
        title='List of commands and what the hell they do (Yes its fucking ass, shut the fuck up)',
        description="This servers prefix is: Idk, something. You just used it, fuck you.\n"
                    "Below are the aliases and descriptions of all commands.\n"
                    "If you don't understand, ask someone who does. Or else just get fucked.",
        color=discord.Color.blurple()
    )

    msg.add_field(
        name='Basic Bot Commands:',
        value='➡ [info, jeffinfo]: `Shows info about Jeff-bot`\n'
              '➡ [prefix]: `Set new prefix for your server`\n'
              '➡ [help]: `Shows this message`\n'
              "➡ [restart, boop]: `Don't you fucking dare touch this. You've been warned`",
        inline=False
    )

    msg.add_field(
        name='Api Commands',
        value='➡ [dad, dadjoke, djoke]: `Gives you a random dad joke`\n'
              '➡ [joke]: `Random joke, categories are: Programming, Misc, Dark, Pun, Spooky, Christmas`\n'
              '➡ [random, uncy]: `Gives a random Uncyclopedia article`\n'
              '➡ [fact]: `Gives a random fact which is probably true, some are really out there or just old`\n'
              '➡ [fm, findm]: `Checks IMDB. Takes a movie name as argument. Gives back ratings of that movie. Ex: <prefix>fm <moviename>`\n'
              '➡ [fs, finds]: `Checks IMDB. Takes a show/series name as argument. Gives back ratings of that show/series. Ex: <prefix>fm <showname>`\n',
        inline=False
    )

    msg.add_field(
        name='Casino commands',
        value='➡ [blackjack, bj]: `Play a round of blackjack. Ex: <prefix>bj 150 (play blackjack with 150 chips)`\n'
              '➡ [coinflip, cf]: `Toss a coin, maybe get lucky. Ex: <prefix>>cf <sideOfCoin>(heads, h, tails, t) <amount>(h=half, a=all)`\n'
              '➡ [jc]: `Register at the casino, basically just adds you to the database so you can gamble.`\n'
              '➡ [gib]: `Ask the casino if you could please get some chips for your gambling addiction`\n'
              '➡ [sjekkels, sj, s]: `See how many chips you currently have`\n'
              '➡ [profile, p]: `See how many chips you currently have`\n'
              '➡ [dice]: `See how many chips you currently have`\n'
              '➡ [rank]: `See how many chips you currently have`\n'
              '➡ [claimall, ca]: `See how many chips you currently have`\n',

        inline=False
    )

    msg.add_field(
        name="Funny commands, or at least I think they're funny",
        value='➡ [beadick, bad]: `Throws a random insult a person mentioned. Insult will be pretty bad`\n'
              '➡ [yoda]: `Fuck off Yoda says`\n'
              '➡ [jooda, jewda]: `Give gold you must, Jewda says`\n'
              '➡ [kill]: `Kill someone, Kill yourself or Kill everyone. Ex: <prefix>kill @mention`\n'
              '➡ [nicht]: `If you know you know`\n'
              '➡ [b2ba]: `Same for this one`\n'
              "➡ [king]: `Let someone know what they're worth`\n"
              "➡ [rip]: `Someone just died. Show some respect`\n",
        inline=False
    )

    msg.set_footer(
        text='Created by: BaronVonBarron#7882'
    )

    msg.set_author(
        name=bot.user.display_name,
        icon_url=bot.user.avatar
    )

    return await ctx.channel.send(embed=msg)
