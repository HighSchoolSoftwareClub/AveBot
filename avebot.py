import discord
import asyncio
import urllib.request
from pathlib import Path
import socket
import datetime
import traceback
import re
import os
import time

client = discord.Client()

def avelog( content ):
    try:
        st = str(datetime.datetime.now()).split('.')[0]
        text = st + ': ' + content
        print(text)
        with open("log.txt", "a") as myfile:
            myfile.write(text+"\n")
        return
    except Exception:
        exit()

@client.event
async def on_ready():
    st = str(datetime.datetime.now()).split('.')[0]
    avelog('Logged in as')
    avelog(client.user.name)
    avelog(client.user.id)
    avelog('------')
    try:
        time.sleep(3)
        await client.change_presence(game=discord.Game(name='run >help'))
        em = discord.Embed(title='AveBot initialized!', description='Hostname: '+socket.gethostname()+'\nLocal Time: '+st+'\nLogs are attached.', colour=0xDEADBF)
        em.set_author(name='AveBot', icon_url='https://s.ave.zone/c7d.png')
        await client.send_message(discord.Object(id='305715263951732737'), embed=em)
        await client.send_file(discord.Object(id='305715263951732737'), "log.txt")
        open('log.txt', 'w').close() # Clears log
    except Exception:
        avelog(traceback.format_exc())
        exit()

@client.event
async def on_message(message):
    try:
        if message.content.startswith('>howmanymessages'):
            client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1    

            await client.edit_message(tmp, 'You have sent {} messages out of the last 100 in this channel.'.format(counter))
        elif message.content.startswith('>get'):
            await client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            link = message.content.split(' ')[1]
            filename = "files/" + link.split('/')[-1]
            urllib.request.urlretrieve(link, filename);
            await client.send_file(message.channel, filename, content=":thumbsup: Here's the file you requested.")
        elif message.content.startswith('>invite'):
            await client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            inviteurl = await client.create_invite(message.channel,max_uses=1)
            em = discord.Embed(title='Invite ready!', description='Here you go: ' + inviteurl.url, colour=0xDEADBF)
            em.set_author(name='AveBot', icon_url='https://s.ave.zone/c7d.png')
            await client.send_message(message.channel, embed=em)
        elif message.content.startswith('>bigly'):
            await client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            letters = re.findall(r'[a-z0-9]', message.content.replace(">bigly ", "").lower())
            biglytext = ''
            for letter in letters:
                biglytext = biglytext+ ":regional_indicator_"+str(letter)+": "
            em = discord.Embed(title='Biglified', description=biglytext, colour=0xDEADBF)
            em.set_author(name='AveBot', icon_url='https://s.ave.zone/bigly.png')
            await client.send_message(message.channel, embed=em)
        elif message.content.startswith('>help'):
            await client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            em = discord.Embed(title='Hello from AveBot!', description='This bot is owned by ao#4273 and is currently running on `'+socket.gethostname()+'` server.\n**>help:** displays this \n**>get <url>:** gets a link and uploads it to discord\n**>dget <url>:** like get, but doesn\'t try to determine filename, also no caching\n**>invite:** generates an invite for this channel one use and unlimited duration\n**>material <name>:** gets an icon from material.io\'s free icons list.\n**>howmanymessages:** Checks how many messages you have in this channel, out of the last 100 ones.\n**>:regional_indicator_b: :regional_indicator_i: :regional_indicator_g: :regional_indicator_l: :regional_indicator_y::** Makes text as big as the hands of the god-emperor.', colour=0xDEADBF)
            em.set_author(name='AveBot', icon_url='https://s.ave.zone/c7d.png')
            await client.send_message(message.channel, embed=em)
        elif message.content.startswith('>dget'):
            await client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            link = message.content.split(' ')[1]
            filename = "files/requestedfile"
            urllib.request.urlretrieve(link, filename);
            await client.send_file(message.channel, filename, content=":thumbsup: Here's the file you requested.")
        elif message.content.startswith('>material'):
            await client.send_typing(message.channel)
            avelog(str(message.author) + " ran " + message.content)
            filename = message.content.split(' ')[1]
            if not filename.startswith('ic_'):
                filename = "ic_" + filename
            if not filename.endswith(('.svg', '.png')):
                filename = filename + "_white_48px.svg"
            link = "https://storage.googleapis.com/material-icons/external-assets/v4/icons/svg/" + filename
            filename = "files/" + filename
            my_file = Path(filename)
            if not my_file.is_file():
                urllib.request.urlretrieve(link, filename);
            await client.send_file(message.channel, filename, content=":thumbsup: Here's the file you requested.")
    except Exception:
        avelog(traceback.format_exc())
        exit()

if not os.path.isdir("files"):
    os.makedirs("files")

if os.path.exists("bottoken"):
    file = open("bottoken", "r") 
    client.run(file.read())
else:
    avelog("No bottoken file found! Please create one. Join discord.gg/discord-api and check out #faq for more info.")