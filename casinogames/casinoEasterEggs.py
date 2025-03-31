from casinogames.casino import get_xp, get_achievement


def sixty_nine(ctx):
    user_name_fr = str(ctx.author.name)
    user_xp = get_xp(user_name_fr)
    user_achievements = get_achievement(user_name_fr)
    if user_xp == 69420:
        if "69" not in user_achievements:
            user_achievements.append("69")
            user_xp += 100
            return f"Congratulations {ctx.author.mention}! You have reached 69420 XP and unlocked the 69 achievement! You have been awarded 69420 XP!"
        return f"Congratulations {ctx.author.mention}! You have reached 69420 XP and unlocked the 69 achievement!"

