import discord
import re
import requests
import platform
import sys
from random import randint
import datetime
from datetime import timedelta, date


platform = platform.system()
if platform == 'Windows':
    file = open('token.txt', 'r')
    log = open('discord_error_rope.log', 'w')
elif platform == 'Linux':
    file = open('/opt/scripts/ropehelper/token.txt', 'r')
    log = open('/tmp/discord_error_rope.log', 'w')

TOKEN = file.read()

client = discord.Client()

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return
            
        if message.content.startswith('!help'):
            msg = """Bot has the following commands
            "!list" displays available roles
            "!add-<rolename>" gives the user chosen role and channel access
            (Use the exact role names from !list)
            "!calendar" generates the next 14 days (Folks can then add emote to whichever date's would suit them) 
            (Can only be used in "peliajat" channels)
            """
            await client.send_message(message.channel, msg)
        
        if message.content.startswith('!list'):
            l = 'Here is a list of game roles in this channel\n'
            for s in client.servers:
                for r in s.roles:
                    if not r.name.startswith('Real') and not r.name.startswith('@everyone'):
                        l += '{0}\n'.format(r) 
            await client.send_message(message.channel, l)  

        if message.content.startswith('!add'):
            flag = False
            for s in client.servers:
                for r in s.roles:
                    if not r.name.startswith('real'):
                        if str(r.name).lower() == str(message.content[5:]).lower():
                            await client.add_roles(message.author, r)
                            msg = 'Added role {0} for user {1}'.format(r, message.author)
                            await client.send_message(message.channel, msg)
                            flag = True
            if flag == False:
                msg = 'Role not found or something else went wrong :shrug:'
                await client.send_message(message.channel, msg)

        if message.content.startswith('!calendar'):
            if 'peliajat' in message.channel.name:
                for i in range(14):
                    date = datetime.datetime.now() + timedelta(days=i)
                    msg = date.strftime('%A %d.%m.')
                    await client.send_message(message.channel, msg)
            else:
                msg = '!calendar is only permitted on "peliajat" -channels'
                await client.send_message(message.channel, msg)

        if message.content.startswith('!git'):
            msg = """Source for this bot can be found at:
            https://github.com/ville-solja/kukkohelper"""
            await client.send_message(message.channel, msg) 

        if message.content.startswith('!roll'):
            totalsum = 0
            msg = ''
            rolls = message.content[6:]
            for roll in rolls.split('+'):
                diesum = 0
                split = re.split('d', roll)
                amount = int(split[0])
                die = int(split[1])
                for i in range(0,amount):
                    diecast = randint(1,die)
                    diesum += diecast
                    msg += '{0}: {1}\n'.format(roll, diecast)
                msg += 'roll sum: {0}\n'.format(diesum)
                totalsum += diesum
            msg += 'total sum: {0}'.format(totalsum)
            await client.send_message(message.channel, msg)

    except:
        e = sys.exc_info()[1]
        log.write(str(e))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for each in client.servers:
        print(each.name)

client.run(TOKEN)