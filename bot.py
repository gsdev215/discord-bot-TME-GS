import discord,sys,os,io,time,datetime,json,asyncio
import config as C
from cogs.utils import checks
from discord.ext import commands

def get_prefix(bot, message): ##first we define get_prefix
    with open('prefixes.json', 'r') as f: ##we open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f) #load the json as prefixes
    try:
    	return prefixes[str(message.guild.id)]
    except:
    	return C.default_prefix

intents = discord.Intents().default()
intents.messages = True
intents.reactions = True
intents.presences = True
intents.members = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False

bot = commands.Bot(
    command_prefix= (get_prefix),
    intents=intents)
@bot.event
async def on_ready():
	print("online")
	
@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('prefixes.json', 'r') as f: #read the file
        prefixes = json.load(f)
    
    g = f"{guild.id}"
    prefixes.pop(g) #find the guild.id that bot was removed from

    with open('prefixes.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)

@bot.command()
@checks.is_admin()
async def setprefix(ctx,prefix:str):
    with open('prefixes.json','r') as f:
        n = json.load(f)
    s = f"{ctx.guild.id}"
    n[s] = prefix
    with open("prefixes.json","w") as f:
        json.dump(n,f)
    await ctx.reply(f"changed prefix in this guild to `{prefix}`")
     
@bot.command()
async def run(ctx,*,c):
	e = f"{eval(c)}"
	await ctx.send(e)
	
if __name__ == "__main__":
	for extension in C.cog:
		try:
			bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")
			      

bot.run(C.token)
