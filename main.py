# Main:
# Where all Discord events are handled

# IMPORTS
import discord
import BOT_module
import VG_module

# Discord Variables--
client = discord.Client()

# Whenever BOT is READY
@client.event
async def on_ready():

    print('Logged In As: ' + client.user.name + "  ID:  " + client.user.id + "\n\n")


# Whenever a MESSAGE is SENT
@client.event
async def on_message(message):

    # Make sure the AUTHOR of the MSG isn't BOT
    if message.author == client.user:
        return

    # Gives a LIST of possible COMMANDS
    if message.content.startswith('>help'):
        await BOT_module.helpBOT(client, message)

    # Tells AUTHOR how many MSGs he has in THIS channel
    if message.content.startswith('>catch'):
        await BOT_module.catchBOT(client, message)

    # Tells BOT to sleep for NUM of SECONDS
    elif message.content.startswith(">sleep"):
        await BOT_module.sleepBOT(client, message)

    elif message.content.startswith(">VG"):
        await VG_module.commandVG(client, message)

# RUNS BOT with Discord KEY
client.run("")  # DISCORD_BOT_TOKEN_HERE
