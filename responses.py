import random
import discord
from discord import Intents
from discord.ext import commands
from aiohttp import request
import json
import requests

def handle_response(message, member_list, author) -> str:
    client = discord.Client(intents=Intents.all())
    api_root = "http://127.0.0.1:5000"
    user = author
    p_message = message.lower()
    
    if p_message.startswith("_hello"):
        return "Hello"
    
    if p_message.startswith("_roll"):
        roll = str(random.randint(1, 100))
        user = user
        return (user + " rolled: " + roll)
    
    if p_message.startswith('_help'):
        
        help_message = ('The following commands are available to you:\n\n'
            ' ? + command   :   Placing a ? in front of a command sends the response to you in a private message instead of posting it to the channel\n\n'
            ' _timeout   :   Prevent bot from asking you to set your class on login for 1 week (You may still use the set command at any time)\n'
            ' _set_class class   :   Set your class the the class you intend to play in Ashes of Creation\n'
            ' _class username   :   shows you what class that user intends to / is playing\n'
            ' _tank   :   Shows a list of all users who play a tank role\n'
            ' _DPS   :   Shows a list of all users who play a DPS role\n'
            ' _Support   :   Shows a list of all users who play a support role\n'
            ' _Healer   :   Shows a list of all users who play as a healer (Cleric)\n'
            ' _find_class class-name   :   Shows a list of all users who play a specific class\n'
            ' _find_true_class class-name   :   Shows a list of all users whos primary class and augment are the same (Example: Tank / Tank)\n'
            '_roll   :   Returns a random number between 1 and 100')
        
        return help_message
    
    if p_message.startswith("_set_class "):
        
        user_data = {'username': str(user)}
        user_class = message[11:]
        user_data['class'] = str(user_class)
        response = requests.post(api_root + '/api/update/member', json=user_data)
        return json.dumps(response.json())
    
    if p_message.startswith("_class "):
        
        get_user = message[7:]
        get_user = str(get_user).lower()
        response = requests.get(api_root + '/api/get-user-class/' + get_user)
        return json.dumps(response.json())
        