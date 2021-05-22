import sys,os,json,asyncio
from discord.ext import commands
import vacefron
import discord
from cogs.utils import checks
import pymongo
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8'] # this is a google public dns server,  use whatever dns server you like here
# as a test, dns.resolver
client = pymongo.MongoClient("mongodb+srv://gsdev1:devpython215@cluster0.v4du6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.discord
n = db.leveling

vac_api = vacefron.Client()

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config as C

class leveling(commands.Cog, name="leveling"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self,message):#n["dis_level"] = {}#n["dis_level"]["834797692802564106"]= None#C.json_dump(f="enable.json", n = n)
    	    for x in n.find({}, {"dis_level":1}):
    	    	print(x)
    	    	if not message.guild.id in x:
    	    		break
    	    		#await self.bot.process_commands(message)
    	    	else:
    	    		pass
    	    if not message.author.bot:
    	       with open('level.json','r') as f:
    	       	users = json.load(f)
    	       await update_data(users, message.author,message.guild,message.author.name)
    	       await add_experience(users, message.author, 4, message.guild,message.author.name)
    	       await level_up(users, message.author,message.channel, message.guild)
    	       with open('level.json','w') as f:
    	       	json.dump(users, f)
    	       #await self.bot.process_commands(message)
    	       return 
    @commands.command(name = "level")
    async def level(self,ctx,user:discord.Member=None):
    	await ctx.send("pls wait..... ")
    	await asyncio.sleep(1)
    	await ctx.message.channel.purge(limit=1)
    	if user is None:
    		user = ctx.author
    		k = C.json_open(f="level.json")
    		o = f"{user.id}"
    		j = k[str(ctx.guild.id)][o]["experience"]
    		l = k[str(ctx.guild.id)][o]["level"]
    		n = C.json_open(f="levels.json")
    		a = n[str(l)]["start_lvl"]
    		b = n[str(l)]["start_end"]
    		c = await vac_api.rank_card(username=str(user),
    		    avatar = user.avatar_url_as(format = "png"),
    		    current_xp=int(j),
    		    next_level_xp = int(b),
    		    previous_level_xp=int(a),
    		    level = int(l),
    		    rank = None,
    		    custom_background = "https://cdn.discordapp.com/attachments/811843136547717132/844475533080789022/photo-1546587348-d12660c30c50.jpeg",
    		    xp_color = "136CF0",
    		    is_boosting = True,
    		    circle_avatar = True
    		)
    		rank_image = discord.File(fp = await c.read(), filename = f"{user.name}_rank.png")
    		await ctx.send(f"{user.name}'s rank in {ctx.guild.name}", file = rank_image)
    	else:
    		k = C.json_open(f="level.json")
    		o = f"{user.id}"
    		j = k[str(ctx.guild.id)][o]["experience"]
    		l = k[str(ctx.guild.id)][o]["level"]
    		n = C.json_open(f="levels.json")
    		a = n[str(l)]["start_lvl"]
    		b = n[str(l)]["start_end"]
    		c = await vac_api.rank_card(username=str(user),
    		    avatar = user.avatar_url_as(format = "png"),
    		    current_xp=int(j),
    		    next_level_xp = int(b),
    		    previous_level_xp=int(a),
    		    level = int(l),
    		    rank = None,
    		    custom_background = "https://cdn.discordapp.com/attachments/811843136547717132/844475533080789022/photo-1546587348-d12660c30c50.jpeg",
    		    xp_color = "136CF0",
    		    is_boosting = True,
    		    circle_avatar = True
    		)
    		rank_image = discord.File(fp = await c.read(), filename = f"{user.name}_rank.png")
    		await ctx.send(f"{user.name}'s rank in {ctx.guild.name}", file = rank_image)

    #@
    #@
    
    @commands.command()
    @checks.is_admin()
    async def dis_level(self,ctx):
    		for l in n.find({}, {"dis_level":1}):
    			if not ctx.guild.id in l:
    				pass
    			else:
    				break 
    			x = n.update_one({"_id":0},{"$set":{f"{ctx.guild.id}": f"{ctx.author.id}"}})
    			
    			await ctx.send(x)
async def update_data(users, user,server,name):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
            users[str(server.id)][str(user.id)]['name'] = name
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
            users[str(server.id)][str(user.id)]['name'] = name

async def add_experience(users, user, exp, server,name):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp
  users[str(user.guild.id)][str(user.id)]['name'] = name

async def level_up(users, user, channel, server):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/4))
  if str(user.guild.id) != '757383943116030074':
    if lvl_start < lvl_end:
      await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
      users[str(user.guild.id)][str(user.id)]['level'] = lvl_end
      
def setup(bot):
    bot.add_cog(leveling(bot))