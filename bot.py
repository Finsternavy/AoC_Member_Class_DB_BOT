from email.headerregistry import ContentTypeHeader
from email.mime import application
import json
from operator import contains
from unicodedata import name
from wsgiref import headers
import discord
from discord import Intents
from discord.ext import commands
from flask import jsonify, session, request
import requests
import responses
import os
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()
api_root = "http://127.0.0.1:5000"
client = discord.Client(intents=Intents.all())
member_list = []

async def send_message(message, user_message, is_private):
    
    try:
        response = responses.handle_response(user_message, member_list, message.author.nick)
        
        if response == 'author':
            await message.author.send(message.author.nick) if is_private else await message.channel.send(message.author.nick)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
        
    except Exception as e:
      print(e)


# add new members, removes members who have left the guild
@client.event
async def update_members(member_list):
    url = api_root + '/api/update/members'
    response = requests.post(url, json=member_list)
    print(response.text)
        


def run_bot():
    TOKEN = os.getenv("TOKEN")
    GUILD = os.getenv("GUILD")
    
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
        
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        
        # current_members = []
        
        # build list of user objects to update database with current users
        for member in guild.members:
            new_member = {}
            new_member['username'] = str(member.nick)
            member_list.append(new_member)
            
        # this features updates the database with new users and removes users who have left the guild
        await update_members(member_list)
            
        
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