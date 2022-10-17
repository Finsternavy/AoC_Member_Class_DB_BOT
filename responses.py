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
        
        help_message = (
            'Example command:\n'
            ' _find rogue   (This is an example of the _find class-name command below.)\n\n'
            ' ? + command   :   Placing a ? in front of a command sends the response to you in a private message instead of posting it to the channel.  You can not execute commands in private chat.\n\n'
            'The following commands are available to you:\n\n'
            ' _set_class class   :   Set your class the the class you intend to play in Ashes of Creation. Example: "_set_class dreadnought"\n'
            ' _class username   :   shows you what class that user intends to / is playing\n'
            ' _tank   :   Shows a list of all users who play a tank role\n'
            ' _DPS   :   Shows a list of all users who play a DPS role\n'
            ' _support   :   Shows a list of all users who play a support role\n'
            ' _healer   :   Shows a list of all users who play as a healer (Cleric)\n'
            ' _find class-name   :   Shows a list of all users who play a specific primary class (8 archetypes)\n'
            ' _find_true class-name   :   Shows a list of all users whos primary class and augment are the same (Example: Tank / Tank)\n'
            ' _roll   :   Returns a random number between 1 and 100\n'
            ' _remind   :   Remind your guild members to set their classes\n'
            ' _class_breakdown   :   Displays a breakdown of the entired guilds class structure')
        
        return help_message
    
    if p_message.startswith("_set_class "):
        
        user_data = {'username': str(user)}
        user_class = message[11:]
        user_data['class'] = str(user_class)
        response = requests.post(api_root + '/api/set-user-class', json=user_data)
        return json.dumps(response.json())
    
    if p_message.startswith("_class "):
        
        get_user = message[7:]
        get_user = str(get_user).lower()
        response = requests.get(api_root + '/api/get-user-class/' + get_user)
        return json.dumps(response.json())
    
    if p_message.startswith('_clear '):
        user_to_clear = message[7:]
        if user == user_to_clear:
            response = requests.post(api_root + '/api/clear-user-class/' + user_to_clear)
            return json.dumps(response.json())
        else:
            response_string = 'Only the user can clear their own class.'
            return json.dumps(response_string)
        
    if p_message.startswith('_class_breakdown'):
        
        # need to add stats for each archetype (Fighter, tanks, rogue, etc..)
        
        response = requests.get(api_root + '/api/guild/class-breakdown')
        guild_stats = response.json()
        
        #list of variables
        true_tanks = guild_stats['true_tanks']
        primary_tanks = guild_stats['primary_tanks']
        augmented_tanks = guild_stats['augmented_tanks']
        true_healers = guild_stats['true_healers']
        primary_healers = guild_stats['primary_healers']
        augmented_healers = guild_stats['augmented_healers']
        true_dps_support = guild_stats['true_dps_support']
        primary_dps_support = guild_stats['primary_dps_support']
        augmented_dps_support = guild_stats['augmented_dps_support']
        total_registered_forces = guild_stats['total_registered_forces']
        
        return_string = (f'true_tanks: {true_tanks} \nprimary_tanks: {primary_tanks} \naugmented_tanks: {augmented_tanks} \ntrue_healers: {true_healers} \nprimary_healers: {primary_healers} \naugmented_healers: {augmented_healers} \ntrue_dps_support: {true_dps_support} \nprimary_dps_support: {primary_dps_support} \naugmented_dps_support: {augmented_dps_support} \ntotal_registered_forces: {total_registered_forces}\n')
        
        return return_string
        
        
    if p_message.startswith('_tank'):
        
        response = requests.get(api_root + "/api/guild/tanks")
        tanks = response.json()
        
        return_string = 'tanks:\n '
        
        for tank in tanks:
            return_string = return_string + f" {tank}\n"
        
        return return_string
    
    
    if p_message.startswith('_dps') or p_message.startswith('_DPS') or p_message.startswith("_support"):
        
        response = requests.get(api_root + "/api/guild/dps-support")
        
        dps_support = response.json()
        
        return_string = 'DPS/Supports:\n'
        
        for member in dps_support:
            return_string = return_string + f" {member}\n"
            
        return return_string
    
    
    if p_message.startswith('_healer'):
        
        response = requests.get(api_root + '/api/guild/healers')
        
        healers = response.json()
        
        return_string = 'Healers:\n'
        
        for healer in healers:
            return_string = return_string + f" {healer}\n"
            
        return return_string
    
    if p_message.startswith("_find "):
        
        search_class = str(message[6:]).lower()
        print(search_class)
        
        classes = ['fighter', 'tank', 'rogue', 'ranger', 'mage', 'summoner', 'cleric', 'bard']
        
        if str(search_class).lower() not in classes:
            return "Invalid class entered.  Please check your spelling and try again."
        
        response = requests.get(api_root + '/api/guild/get-class/' + search_class)
        
        players = response.json()
        
        return_string = f'{search_class.capitalize()}s:\n'
        
        if not players:
            return_string = "No one in the guild plays that class.  :("
            return return_string
        
        for player in players:
            return_string = return_string + f' {player}\n'
            
        return return_string
        
    if p_message.startswith("_find_true "):
        
        search_class = str(message[11:]).lower()
        
        classes = ['fighter', 'tank', 'rogue', 'ranger', 'mage', 'summoner', 'cleric', 'bard']
        
        if str(search_class).lower() not in classes:
            return "Invalid class entered.  Please check your spelling and try again."
        
        response = requests.get(api_root + '/api/guild/get-true-class/' + search_class)
        
        players = response.json()
        
        return_string = f'True {search_class.capitalize()}s:\n'
        
        if not players:
            return_string = f"No one in the guild plays a true {search_class.capitalize()}.  :("
            return return_string
        
        for player in players:
            return_string = return_string + f' {player}\n'
            
        return return_string
        
    if p_message.startswith("_remind"):
        return "Don't forget to set your class for Ashes of creation! Type '_set_class ' then the name of the class you want to play in AoC to set your class! Type '_help' for assistance."