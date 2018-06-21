import discord
import datetime
from datetime import timedelta, date

file = open('token.txt', 'r')
TOKEN = file.read()

client = discord.Client()

@client.event
async def on_message(message):
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


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    for each in client.servers:
       print(each.name)

client.run(TOKEN)