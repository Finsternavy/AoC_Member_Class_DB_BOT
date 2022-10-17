import json
from operator import contains
import discord
from discord import Intents
from discord.ext import commands
from flask import jsonify, session, request
import requests
import responses
import os
from dotenv import load_dotenv
from datetime import datetime, time, timedelta
import asyncio

load_dotenv()
api_root = "http://127.0.0.1:5000"
client = discord.Client(intents=Intents.all())
member_list = []
send_list = []
WHEN = time(23, 24, 0) # 11:20 PM

async def send_message(message, user_message, is_private):
    
    try:
        response = 'default'
        # Check if user is trying to input a command in direct chat instead of in the guild chat
        print(message.author.nick)
        try:
            if message.author.nick:
                print(message.content)
                response = responses.handle_response(user_message, member_list, message.author.nick)
                
        except Exception as e:
            response = 'Commands do not work in private messages. Please input command in the guild server chat.'
        
        if response == 'author':
            await message.author.send(message.author.nick) if is_private else await message.channel.send(message.author.nick)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
        
    except Exception as e:
      print(e)
      


# add new members, removes members who have left the guild
async def update_members(member_list):
    print(member_list)
    url = api_root + '/api/update/members'
    response = requests.post(url, json=member_list)
    print(response.text)



def run_bot():
    TOKEN = os.getenv("TOKEN")
    GUILD = os.getenv("GUILD")
    GEN_CHANNEL = os.getenv("GEN_CHANNEL")
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
        
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        
        # current_members = []
        
        # build list of user objects to update database with current users
        for member in guild.members:
            if str(member) != 'AoC Guild Bot#1463':
                print(member)
                new_member = {}
                new_member['username'] = str(member.nick)
                send_list.append(member)
                member_list.append(new_member)
            
        # this features updates the database with new users and removes users who have left the guild
        await update_members(member_list)
        
        # Reminds users to set their class when the bot comes online (Also available from command _remind)
        channels = client.get_channel(int(GEN_CHANNEL))
        await channels.send("Don't forget to set your class for Ashes of creation! Type '_set_class ' then the name of the class you want to play in AoC to set your class! Type '_help' for assistance.")
            
        
    @client.event
    async def on_message(message):
        # if the author is the bot, don't do anything
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f"{username} said: '{user_message}' ({channel})")
        
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
        
    client.run(TOKEN)