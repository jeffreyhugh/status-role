import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!!"))

@bot.event
async def on_ready():
    print("{} is logged in and ready!".format(bot.user))

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


    # Check to make sure the status changed before doing anything
    if beforeActivity != afterActivity:
        print("{} updated activity: {} -> {}".format(before.name, beforeActivity, afterActivity))

        # Iterate through roles, choose and assign
        beforeRoles = before.roles
        beforeRolesCheck = beforeRoles

        for r in before.guild.roles:
            if r.name == afterActivity:
                # If there's a role with the same name as what they're doing
                beforeRoles.append(r)

            if r.name == beforeActivity:
                # If there's a role with the same name as what they were doing
                beforeRoles.remove(r)

        # This might throw an error, but it will ignore the error.
        await before.edit(roles=beforeRoles)

bot.run("YOUR TOKEN GOES HERE")
