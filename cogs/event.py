import sys,os,json,asyncio,time,datetime,aiml
from discord.ext import commands
import discord
from cogs.utils import checks
try:
    preferred_clock = time.perf_counter
except AttributeError:# Earlier than Python 3.
	preferred_clock = time.clock

#<----------AIML-----------------> 
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")
#<--------------------------------------->
	
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config as C
    

#<----------SNIPE------------>
snip_message = {}
snip_author = {} 
#<--------------------------------------->

#-------------------------

class event(commands.Cog, name="event"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_delete(self,message):
    	snip_message[message.channel.id] = message.content.lower ()
    	snip_author[message.channel.id] = message.author.name
    @commands.Cog.listener()
    async def on_message(self,message):
    	if message.author.bot:
    		return
    	else:
    		if self.bot.user.mentioned_in(message):
    			msg=message.content.lower()
    			respons = kernel.respond(msg)
    			await message.reply(respons)
    		else:
    			return
    		
    @commands.command()
    async def snipe (self,ctx):
    	msg = snip_message[ctx.channel.id]
    	by = snip_author[ctx.channel.id]
    	snip = discord.Embed(title = f"Last deleted message in this channel ", description = f"**{msg}** by:- {by}\n\n`I have strong memory then humman haha`")
    	await ctx.send (embed = snip)
    	

    
def setup(bot):
    bot.add_cog(event(bot))
    