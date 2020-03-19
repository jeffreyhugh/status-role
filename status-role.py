import discord
from discord.ext import commands
import asyncio
import json

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!!"))

@bot.event
async def on_ready():
    print("{} is logged in and ready!".format(bot.user))

@bot.command(name="role")
async def _role(ctx):

    try:
        with open("roles.json","r") as f:
            roleRedirects = json.load(f)
    except FileNotFoundError:
        roleRedirects = {}

    currentRoles = ctx.guild.me.roles
    gameRole = None
    for r in currentRoles:
        if r.name == "@everyone":
            continue
        elif r.name == bot.user.name:
            continue
        else:
            gameRole = r

    print(gameRole)
    if gameRole == None:
        await ctx.send("Please assign me a role before using this command")
        return

    try:
        mentioned = ctx.message.mentions[0]
    except IndexError:
        await ctx.send("Please mention a user with this command")
        return

    print(roleRedirects)

    try:
        activity = mentioned.activity.name
    except AttributeError:
        await ctx.send("{} is not currently playing a game".format(mentioned.name))
        return

    roleRedirects[activity] = gameRole.id

    await ctx.send("Successfully linked `{}` to role ID `{}`. Please don't forget to remove my extra role once you're done with this command.".format(activity, gameRole.id))

    with open("roles.json","w") as f:
        json.dump(roleRedirects, f)

def checkForLink(status):
    try:
        with open("roles.json","r") as f:
            roleRedirects = json.load(f)
    except FileNotFoundError:
        roleRedirects = {}

    try:
        return roleRedirects[status]
    except IndexError:
        return None

@bot.event
async def on_member_update(before, after):
    '''Listen for member change events (status changes are included in this)'''

    # If they didn't have a status before, this will catch that error.
    try:
        beforeActivity = before.activity.name
    except AttributeError:
        beforeActivity = None

    try:
        afterActivity = after.activity.name
    except AttributeError:
        afterActivity = None

    '''ignoreCharacters = ["®"]
    for c in ignoreCharacters:
        if beforeActivity != None:
            beforeActivity = beforeActivity.strip(c)
        if afterActivity != None:
            afterActivity = afterActivity.strip(c)'''

    # Check to make sure the status changed before doing anything
    if beforeActivity != afterActivity:
        print("{} updated activity: {} -> {}".format(before.name, beforeActivity, afterActivity))

        # Iterate through roles, choose and assign
        beforeRoles = before.roles

        for r in before.guild.roles:
            if r.name == afterActivity:
                # If there's a role with the same name as what they're doing
                beforeRoles.append(r)

            if r.name == beforeActivity:
                # If there's a role with the same name as what they were doing
                beforeRoles.remove(r)

        if beforeActivity != None:
            beforeLink = checkForLink(beforeActivity)
        if afterActivity != None:
            afterLink = checkForLink(afterActivity)

        if afterActivity != None:
            beforeRoles.append(before.guild.get_role(afterLink))
        if beforeActivity != None:
            beforeRoles.remove(before.guild.get_role(beforeLink))

        # This might throw an error, but it will ignore the error.
        await before.edit(roles=beforeRoles)

bot.run("YOUR TOKEN GOES HERE")
