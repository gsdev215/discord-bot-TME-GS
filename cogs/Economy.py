import sys,os,json,asyncio,random
from discord.ext import commands
from discord.ext.commands import command 
import discord
from cogs.utils import checks

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config as C

class Economy(commands.Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot
        
    @command()
    async def create(self,ctx):
    	n = C.json_open(f="economy.json")
    	user = f"{ctx.author.id}"
    	if not user in n:
    		n[user]={}
    		n[user]["bank"]=0
    		n[user]["wallet"]=0
    		C.json_dump(n=n,f="economy.json")
    		await ctx.send("create account")
    	elif user in n:
    		await ctx.send("hey stupid user! do you have memory problem you already have an account **lol**")
    		
    @command(name="bal",aliases=["wallet","acc","account","money"])
    async def balance(self,ctx,users:discord.Member=None):
    	n  = C.json_open(f="Economy.json")
    	if users is None and f"{ctx.author.id}" in n:
    		user = f"{ctx.author.id}"
    		bank = n[user]["bank"]
    		wallet = n[user]["wallet"]
    		em = discord.Embed(title=f'{ctx.author.name} Balance',color = discord.Color.green())
    		em.add_field(name="Wallet Balance", value=wallet)
    		em.add_field(name='Bank Balance',value=bank)
    		await ctx.send(embed= em)
    	elif users is None and not f"{ctx.author.id}" in n:
    		await ctx.send(f"Hey you user! do you think without creating account in bank you can see your bank balance. use `create` command")
    	elif not f"{users.id}" in n:
    		await ctx.send(f"Sorry user, I can't find that user having bank account, go and teach him to create one and try again")
    	else:
    		user = f"{users.id}"
    		bank = n[user]["bank"]
    		wallet = n[user]["wallet"]
    		em = discord.Embed(title=f'{users.name} Balance',color = discord.Color.green())
    		em.add_field(name="Wallet Balance", value=wallet)
    		em.add_field(name='Bank Balance',value=bank)
    		await ctx.send(embed= em)
    		
    @command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self,ctx):
    	n = C.json_open("economy.json")
    	if not f"{ctx.author.id}" in n:
    		await ctx.send("I am tried saying that without creating an account you can't earn,check,eat,etc.. money ")
    	else:
    		r = random.randint(10,1000)
    		q = ["Billy","Bob","Thomas","Random rich guy","sab",
    		    "Logisch_JoJo","Gs.dev","Luke","Tovade","Shalev","MrMac","God"]
    		a = random.choice(q)
    		n = C.json_open(f="economy.json")
    		n[f"{ctx.author.id}"]["wallet"]+=r
    		C.json_dump(n=n,f="economy.json")
    		await ctx.send(f"{a} gave you {r}$")
    		
    @beg.error
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
        	em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red ())
        	await ctx.send(embed=em)
        	
    @command()
    async def shop(self,ctx,pg=None):
    	
    
#@
  
def setup(bot):
    bot.add_cog(Economy(bot))