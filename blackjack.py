import json


def join(ctx):
    with open('chips.json', 'r') as f:
        chips = json.load(f)

    chips[str(ctx.author.id)] = '0'

    with open('chips.json', 'w') as f:
        json.dump(chips, f, indent=4)

# function for getting cards needs to be addded
