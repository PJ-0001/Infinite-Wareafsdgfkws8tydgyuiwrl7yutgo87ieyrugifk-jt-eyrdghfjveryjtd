



ongoing_searches = {}

log_channel = None
temporary_whitelist = {} # Ignore
blacklist = {}
kick_logs_channel = None

# Keep this here!



# Importd
import requests
import discord
import random
import socket
import asyncio
import datetime
import base64
from discord.ext import commands
import os
from datetime import datetime

import json
import subprocess

from discord import VoiceChannel



with open('Config.json', 'r') as config_file:
    config = json.load(config_file)

BOT_TOKEN = config['BOT_TOKEN']
owner_id = int(config['owner_id'])
prefix = config['prefix']
presence_message = config['presence']
IPINFO_API_TOKEN = '7e2934833edb11'  
RAPIDAPI_KEY = 'f2cd0bb930msh67db8751fac7eb1p1a2e2fjsnb3b5580f8486' 




intents = discord.Intents.all()

bot = commands.Bot(command_prefix=prefix, intents=intents, status=discord.Status.do_not_disturb, help_command=None)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name=presence_message))




@bot.slash_command(name="whitelist")
@commands.check(lambda ctx: ctx.author.id == owner_id)
async def whitelist(ctx):
    if whitelisted_users:
        whitelist_message = "Whitelisted Users:\n"
        
        for user_id in whitelisted_users:
            user = await bot.fetch_user(user_id)
            if user:
                if user_id in temporary_whitelist:
                    expiration_date = temporary_whitelist[user_id]
                    whitelist_message += f"{user.name}#{user.discriminator} (ID: {user.id}) - Subscribed until {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
                else:
                    whitelist_message += f"{user.name}#{user.discriminator} (ID: {user.id})\n"
            else:
                whitelist_message += f"User with ID {user_id} not found\n"
                
        await ctx.respond(whitelist_message)
    else:
        await ctx.respond("No users are currently whitelisted.")

def save_temp_whitelist():
    with open("temporary_whitelist.txt", "w") as file:
        for user_id, expiration_date in temporary_whitelist.items():
            user_info = f"{user_id} - Subscribed until {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            file.write(user_info)




def save_whitelist(whitelist):
  with open("whitelist.txt", "w") as file:
    for user_id in whitelist:
      file.write(str(user_id) + "\n")


def load_whitelist():
  try:
    with open("whitelist.txt", "r") as file:
      return [int(line.strip()) for line in file.readlines()]
  except FileNotFoundError:
    return []

whitelisted_users = load_whitelist()

@bot.slash_command(name="addwhitelist", description = "Adds people to the whitelist of the product.")
@commands.check(lambda ctx: ctx.author.id == owner_id)
async def addwhitelist(ctx, user_id: str):
    if user_id not in whitelisted_users:
        whitelisted_users.append(user_id)
        save_whitelist(whitelisted_users)
        await ctx.respond(f"User ID {user_id} has been whitelisted.")
    else:
        await ctx.respond(f"User ID {user_id} is already whitelisted.")



@bot.slash_command(name="unwhitelist", description = "Just a way of unwhitelisting people")
@commands.check(lambda ctx: ctx.author.id == owner_id)
async def unwhitelist(ctx, user_id: str):
  if user_id in whitelisted_users:
    whitelisted_users.remove(user_id)
    save_whitelist(whitelisted_users)
    await ctx.respond(f"User ID {user_id} has been removed from the whitelist.")
  else:
    await ctx.respond(f"User ID {user_id} is not in the whitelist.")


def is_whitelisted(ctx):
    if ctx.author.id in whitelisted_users or ctx.author.id == owner_id:
        return True
    else:
        non_whitelisted_message = "Hello, it looks like you don't have a subscription. Please purchase one at "
        asyncio.create_task(ctx.respond(non_whitelisted_message))
        return False




@bot.slash_command(name="stopsearch", description="Stop the ongoing search")
async def stop_search(ctx):
    
    if ctx.author.id in ongoing_searches:
        # Cancel the ongoing search task
        ongoing_searches[ctx.author.id].cancel()
        del ongoing_searches[ctx.author.id]
        await ctx.respond("Search has been stopped.")
    else:
        await ctx.respond("No ongoing search to stop.")

async def perform_search(ctx, user, github_url):
    lines = []

    for line in data.splitlines():
        if user in line:
            lines.append(line)

    if lines:
        for line in lines:
            await ctx.send(f"```{line}```")
    else:
        await ctx.send("We are sorry, but the data was not found in the databases")


@bot.slash_command(name="search", description="This is the way you grab the IP using the Fivem databases")
@commands.check(is_whitelisted)
@commands.cooldown(1, 5, commands.BucketType.user)
async def search(ctx, user: str):
    await ctx.respond("Sending it in 5 seconds")

    global data
    github_url = "https://cdn.discordapp.com/attachments/1170476032621547583/1170476089357897748/jemoeder.txt?ex=65592dce&is=6546b8ce&hm=c718c0264bda0437f7341f185eb557e9dd299af78ea2e54fb7b20d6127756359&"
    data = requests.get(github_url).text


    ongoing_searches[ctx.author.id] = bot.loop.create_task(perform_search(ctx, user, github_url))












bot.run(BOT_TOKEN)