# Body Module:
# Things that give a bot meaning!

# IMPORTS
import asyncio
import TOOL_module

# Gives a LIST of possible COMMANDS
async def helpBOT(client, message):

    await client.send_message(message.channel, "**Computer Bot Commands:**\n**>help**  ~  *list of general commands*"
    "\n**>catch** ~ *number of messages from you in this channel*\n**>sleep** ~ *let this BOT take a breather*"
    "\n**>VG help** ~ *list of VG module commands*")

# Tells AUTHOR how many MSGs he has in THIS channel
async def catchBOT(client, message):
    counter = 0
    tmp = await client.send_message(message.channel, "Calculating messages...")
    async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
    await client.edit_message(tmp, "You have " + str(counter) + " messages!")

# Tells BOT to sleep for NUM of SECONDS
async def sleepBOT(client, message):

    COMMAND = message.content.split()  # Split the command up [1] = '>sleep', [2] = 'AMOUNT_OF_SECONDS', [3+] = 'TRASH'

    if (len(COMMAND) > 1):  # CHECK to see if we are GIVEN a specific TIME
        NUM = COMMAND[1]  # NUM is SET to the SECOND key word of the COMMAND

        if (TOOL_module.isIntTOOL(NUM) == True):
            NUM = int(NUM)
            NUM = abs(NUM)

            if NUM > 3600:
                NUM = 3600

        else:
            NUM = False

    else:
        NUM = 5

    if NUM == False:
        await client.send_message(message.channel, "Can't go to sleep to " + str(COMMAND[1]) + "!")

    else:
        await client.send_message(message.channel, "Going to sleep for " + str(NUM) + " seconds good night... :sleeping:")
        await asyncio.sleep(NUM)
        await client.send_message(message.channel, "Done sleeping! :raised_hands:")
