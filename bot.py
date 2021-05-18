import discord,sys,os,io,time,datetime,json,asyncio,aiohttps
import config as C
from .cogs.utils import checks 
from discord.ext import commands

def get_prefix(client, message): ##first we define get_prefix
    with open('prefixes.json', 'r') as f: ##we open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f) #load the json as prefixes
    return prefixes[str(message.guild.id)] 

bot = commands.Bot(
    command_prefix= (get_prefix),
    )
@bot.event
async def on_guild_join(guild): #when the bot joins the guild
    with open('prefixes.json', 'r') as f: #read the prefix.json file
        prefixes = json.load(f) #load the json file

    prefixes[str(guild.id)] = C.default_prefix #default prefix

    with open('prefixes.json', 'w') as f: #write in the prefix.json "message.guild.id": "bl!"
        json.dump(prefixes, f, indent=4) #the indent is to make everything look a bit neater

@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('prefixes.json', 'r') as f: #read the file
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from

    with open('prefixes.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)

@bot.command()
@checks.is_admin()
async def setprefix(ctx,prefix:str):
    with open('prefixs.json','r+') as f:
        n = json.load(f)
    n[str(ctx.guild.id)] = prefix
    await ctx.reply(f"changed prefix in this guild to `{prefix}`")
