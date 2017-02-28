# VG Module:
# Functions using the VG API. Functions using Discord libraries will be marked by, "!!!DISCORD!!!", in their description.

# IMPORTS
import gamelocker
import datetime
import TOOL_module as tools

# VG Variables-- Use #1 = , Use #2 = Object Oriented
keyVG = "VG_API_TOKEN_HERE"
apiVG = gamelocker.Gamelocker(keyVG).Vainglory()  # Use #1

# apiObjectVG = gamelocker.Gamelocker(keyVG)  # Use #2
# clientVG = v.newClient()  # Use #2


# Will get the COMMAND given and EXECUTE the according FUNCTION
async def commandVG(client, message):
    COMMAND =  message.content.split()  # SPLIT up the MESSAGE to form the COMMAND

    # Check the SIZE of the COMMAND to narrow down the POSSIBILITIES
    if len(COMMAND) == 1:  # >VG
        await client.send_message(message.channel, "**>VG** ~ *Command used in a model for Computer Bot.*"
        "\n**>VG help** ~ *for a list of VG commands*")
    elif len(COMMAND) == 2:
        if str(COMMAND[1]) == "help":  # >VG help
            await client.send_message(message.channel, "**(R) = required input - (O) = optional input**\n**>VG** ~ Command used in a model for Computer Bot. "
        "\n**>VG help** ~ *for a list of commands*\n**>VG player NAME** ~ *Check if IGN is in VG database! ~ NAME - (R)In game name ~*\n**>VG performance NAME DAYS** ~ *Check match performance in a range of days ~ NAME - (R)In game name, DAYS - (O)Day range ~*")
        else:
            await client.send_message(message.channel, "That isn't a command for **>VG**!\n**>VG** ~ *for a list of VG commands*")
    elif len(COMMAND) == 3:  # >VG player
        if str(COMMAND[1]) == "player":
            await client.send_message(message.channel, getIDVG(COMMAND[2]))
        elif str(COMMAND[1]) == "performance":  # >VG performance NAME
            msg = await client.send_message(message.channel, "Looking at " + COMMAND[2] + " match history from the past 7 days... :eyes:")
            await client.edit_message(msg, getPlayerPerformanceVG(COMMAND[2]))
        else:
            await client.send_message(message.channel, "That isn't a command for **>VG**!\n**>VG** ~ *for a list of VG commands*")
    elif len(COMMAND) == 4:
        if str(COMMAND[1]) == "performance":  # >VG performance NAME DAYS
            if tools.isIntTOOL(COMMAND[3]) == True:
                days = int(COMMAND[3])
                if days > 93:
                    days = 93
                if days <= 0:
                    days = 1
                msg = await client.send_message(message.channel, "Looking at " + COMMAND[2] + " match history from the past " + str(days) + " days... :eyes:")
                await client.edit_message(msg, getPlayerPerformanceVG(COMMAND[2], days))
            else:
                await client.send_message(message.channel, "**" + str(COMMAND[3]) + "** *isn't a valid date span!*")
    else:
        await client.send_message(message.channel, "That isn't a command for **>VG**!\n**>VG** ~ *for a list of VG commands*")

# Will CHECK if NAME is VALID. Will RETURNS True or False if TYPE = 0, if TYPE = 1 returns ID or False.
def getIDVG(name, type=0):
    name = str(name)  # Convert NAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.datetime.today()
    daterange = str(datenow - datetime.timedelta(days=7)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.datetime.today()) + "T00:00:00Z"  # CURRENT DATE

    try:
        matches = apiVG.matches({"filter[createdAt-start]": "2017-02-16T12:00:00Z", "page[limit]": 2, "filter[playerNames]": name})
        for r in matches[0].rosters:
            for p in r.participants:
                if p.player.name == name:
                    if type == 0:  # Returns TRUE when name is FOUND
                        return True
                    elif type == 1:  # Returns ID when name is FOUND
                        return p.player.id

    except:  # Returns FALSE whenever an ERROR occurs
        return False

# Will get VG GAME MATCHES according to NAME.
def getGameMatchesVG(name):
    name = str(name)  # Converts NAME to STRING to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.datetime.today()
    daterange = str(datenow - datetime.timedelta(days=7)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.datetime.today()) + "T00:00:00Z"  # CURRENT DATE

    try:  # Tries to FIND PLAYER matches in NA servers
        mathes = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]" : 50, "sort" : "createAt", "filter[playerNames]" : name})
    except:
        try:  # Tries to FIND PLAYER matches in EU servers
            matches = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]" : 50, "sort" : "createAt", "filter[playerNames]" : name})
        except:
            print("!!!SOMETHING WENT HORRIBLY WRONG WHILE TRYING TO FETCH VG MATCHES FOR " + name + "!!!")

# GETS a PLAYERS LIFE time INFORMATION with ID. ID = ID or NAME for player, givenname = If True then ID is actually a NAME, server = Server to work with
def getPlayerInfoVG(ID, givenname=False, server="na"):
    ID = str(ID)  # Convert ID to a STRING to prevent errors

    if givenname == True:  # Checks to see if ID is actually a NAME if so then TURN it into a ID
        ID = str(getIDVG(ID, type=1))

    info = apiVG.player(ID)
    return info

def getPlayerPerformanceVG(name, days=7, type=0):
    name = str(name)  # Convert NAME to STRING to prevent errors
    days = int(days)  # Convert DAYS to INT to prevent errors

    # ADD when FETCHING from VG API!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=days)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    try:
        matches = apiVG.matches({"filter[createdAt-start]": daterange, "page[limit]": 50, "filter[playerNames]": name})
    except:
        return "Couldn't get any matches for **" + name + "** from the past " + str(days) + " days!"

    playerdata = []
    for match in matches:
        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    playerdata.append(participant.stats)

    for data in playerdata:
        print(data)

    return "Something happend!!!"