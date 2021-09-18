import ButtonPaginator
import sys,os,json,asyncio,time,datetime,math 
from discord.ext import commands
import discord
from typing import Union
from cogs.utils import checks
from discord_components import Button, ButtonStyle, InteractionType
from cogs.modules.button import buttons , button2
import cogs.modules.button as B

#<--------------------------->
def calculate(exp):
    o = exp.replace('×','*')
    o = o.replace('÷','/')
    o = o.replace("π","3.1415926")
    o = o.replace("³","**3")
    o = o.replace("²","**2")
    o = o.replace("^","**")
    o = o.replace("√","math.sqrt")
    result=''
    try:
        result = str(eval(o))
    except:
        result='An error occurred.'
    return result
#<-------------------------->

#<--------------------------->
def k(k,res,expression,delta):
	if k:
	       f = discord.Embed(title=f'{res.author.name}\'s calculator ', description=expression, timestamp=delta)
	       return res.respond(content='',embed=f, components=buttons, type=7)
	else:
	   	f = discord.Embed(title=f'{res.author.name}\'s calculator ', description=expression, timestamp=delta)
	   	return res.respond(content='',embed=f, components=button2, type=7)

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config as C

class Tile: 
	def __init__(self, owner:Union[discord.Member, None]=None):
		self.owner=owner

	def __repr__(self):
		if self.owner==None:
			return 'empty'
		return self.owner.name
	def __eq__(self, other):
		return self.owner==other.owner

class TTTGame:
	def __init__(self, bot, ctx, players: tuple):
		self.bot=bot
		self.channel=None
		self.ctx=ctx

		self.players=players
		self.players_dynamic=list(self.players) #used for turn order to swap the players
		self.state=[Tile()]*9

		self.buttons=[Button(emoji='⬛', id=i+1) for i in range(9)]
		self.buttons_inline=None #it's annoying to work with a multidimensional matrix 
		#so we have a flat version and a the version that will be used on the bot
		self.turn_owner=self.players[0]
		self.message=None

	def update_inline_buttons(self):
		self.buttons_inline=[self.buttons[i:i + 3] for i in range(0, len(self.buttons), 3)]

	async def start(self):
		self.update_inline_buttons()
		self.message=await self.ctx.send(content=f'Game has started, {self.players[0].mention}, your turn first', components=self.buttons_inline)
		await self.take_turn(self.turn_owner)

	def check_win(self):
		state=self.state
		winning_combos=[[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
		player_1_owned=[i for i in range(9) if self.state[i].owner==self.players[0]]
		player_2_owned=[i for i in range(9) if self.state[i].owner==self.players[1]]
		for combo in winning_combos:
			if set(combo).issubset(set(player_1_owned)) or set(combo).issubset(set(player_2_owned)):
				return True
		if all([tile.owner for tile in state]): #check for full board
			return None
		return False

	async def take_turn(self, player):
		def check(res):
			return res.user.id == player.id and res.channel == self.ctx.channel and res.component.label == None

		try:
			res = await self.bot.wait_for("button_click", check=check, timeout=6000)

			button_pos=int(res.component.id)

			await res.respond(type=6)
			player_=res.user
			await self.process_turn(player_, button_pos-1)
		except asyncio.TimeoutError:
			await self.ctx.send("Game ends in a draw because you were taking too long. Like come on. It's just Tic Tac Toe, not chess")

	async def process_turn(self, player: discord.Member, position: int): 
		self.state[position]=Tile(player)
		if player==self.players[0]:
			self.buttons[position]=Button(style=ButtonStyle.blue, emoji='❎', id=self.buttons[position].id, disabled=True)
		else:
			self.buttons[position]=Button(style=ButtonStyle.red, emoji='⭕', id=self.buttons[position].id, disabled=True)
		self.update_inline_buttons()
		await self.message.edit(components=self.buttons_inline)


		win=self.check_win()
		if win:
			embed=discord.Embed(title='Winner!', description=f'{player.mention}, you win this game of **Tic Tac Toe**', color=0x53cc74)
			embed.set_author(name="Test Bot")
			self.buttons=[Button(id=button.id, emoji=button.emoji, style=button.style, disabled=True) for button in self.buttons]
			self.update_inline_buttons()
			await self.message.edit(content='Game Over', embed=embed, components=self.buttons_inline)
			return
		if win==None:
			embed=discord.Embed(title='Draw', description=f'Nobody wins this game of **Tic Tac Toe**', color=0x53cc74)
			embed.set_author(name="test Bot" )
			self.buttons=[Button(id=button.id, emoji=button.emoji, style=button.style, disabled=True) for button in self.buttons]
			self.update_inline_buttons()
			await self.message.edit(content='Game Over', embed=embed, components=self.buttons_inline)
			return
		self.players_dynamic.reverse()
		self.turn_owner=self.players_dynamic[0]

		await self.message.edit(content=f'{self.turn_owner.mention}, your turn')

		await self.take_turn(self.turn_owner)
		
class button(commands.Cog, name="button"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command ()
    async def calc(self,ctx):
    	m = await ctx.send(content='Loading Calculators...')
    	expression='None'
    	ex = f"{expression}"
    	r = True
    	num = ["1","2","3","4","5","6","7","8","9","0"]
    	delta = datetime.datetime.utcnow()+ datetime.timedelta(minutes=5)
    	e = discord.Embed(title=f'{ctx.author.name}\'s Calculator',description=ex,timestamp=delta)
    	await m.edit(components=buttons, embed=e)
    	while m.created_at < delta:
    	   res = await self.bot.wait_for('button_click')
    	   if res.author.id == int(ctx.author.id) and res.message.embeds[0].timestamp < delta:
    	       expression = res.message.embeds[0].description
    	       if expression == "None" or expression == "Error":
    	       	expression=''
    	       if res.component.label == 'Exit':
    	           await res.respond(content='Calculator Closed', type=7)
    	           break
    	       elif res.component.label == '←':
    	       	expression=expression[:-1]
    	       elif res.component.label == 'Clear':
    	       	expression='None'
    	       elif res.component.label == "Scientific calculator":
    	       	r = False
    	       elif res.component.label == "Normal calculator":
    	       	r = True
    	       elif res.component.label == '=':
    	       	expression = calculate(expression)
    	       elif res.component.label == "(":
    	       	ex = list(expression)
    	       	if ex[-1] in ["+","-","÷","×"]:
    	       		expression+="("
    	       	else:
    	       		expression+="×("
    	       elif res.component.label == ")":
    	       	ex = list(expression)
    	       	if ex[-1] in ["+","-","÷","×"]:
    	       		expression=expression[:-1]
    	       		expression+=")"
    	       	else:
    	       		expression+=")"
    	       elif res.component.label == "x³":
    	       	ex = list(expression)
    	       	if ex[-1] in ["+","-","÷","×"]:
    	       		expression=expression[:-1]
    	       		expression+="+0³"
    	       	else:
    	       		expression+="³"
    	       elif res.component.label == "√":
    	       	ex = list(expression)
    	       	if ex[-1] in ["+","-","÷","×","."]:
    	       		expression=expression[:-1]
    	       		expression+="√("
    	       	else:
    	       		expression+="*√("
    	       elif res.component.label == "^":
    	       	ex = list(expression)
    	       	if ex[-1] in ["+","-","÷","×","."]:
    	       		expression=expression[:-1]
    	       		expression+="^("
    	       	elif not ex[-1] in num:
    	       		expression+="0^("
    	       	else:
    	       		expression+="^("
    	       elif res.component.label in num or res.component.label in ["+","-","÷","×",".","00"]:
    	       	expression+=res.component.label
    	       await k(r,res,expression,delta)
    	       
    @commands.command()
    async def ttt(self,ctx, player: discord.Member):
	    embed=discord.Embed(title='✉️Invitation!✉️', description=f'{player.mention}, {ctx.author.mention} has challenged you to a game of **Tic Tac Toe**. \n\nPress the button within the next minute to start the game. \n\n*Remember that if you don\'t accept, you might lose a friend~*', color=0x53cc74)
	    embed.set_author(name="Test Bot")
	    button=Button(label='Accept Tic Tac Toe Invite', style=ButtonStyle.green, emoji='☑️')
	    m=await ctx.send(embed=embed, components=[button])
	    def check(res):
		    return player.id == res.user.id and res.channel == ctx.channel
	    try: 
		    res = await self.bot.wait_for("button_click", check=check, timeout=60)
		    if res.component.label=='Accept Tic Tac Toe Invite':
			    game=TTTGame(self.bot, ctx, (ctx.author, player))
			    await m.delete()
			    await game.start()
	    except asyncio.TimeoutError:
		    button=Button(label='Expired Invite :(', style=ButtonStyle.red, emoji='❎', disabled=True)
		    await m.edit(components=[button])

    @commands.command ()
    @checks.is_admin()
    async def setup(self,ctx):
    	delta = datetime.datetime.utcnow()+ datetime.timedelta(minutes=1)
    	m = await ctx.send(content="For more info use .guide",components=B.setup(ctx))
    	def check(res):
    		return ctx.author.id == res.user.id and res.channel == ctx.channel
    	while m.created_at < delta:
    		res = await self.bot.wait_for('button_click',check = check,timeout=70)
    		if res.component.label == "Leveling [OFF]":
    			n=C.json_open(f="log.json")
    			n["level"].append(f"{ctx.guild.id}")
    			C.json_dump(f="log.json",n=n)
    		elif res.component.label == "Leveling [ON]":
    			n=C.json_open(f="log.json")
    			print(n ["level"])
    			n["level"].remove(f"{ctx.guild.id}")
    			C.json_dump(f="log.json",n=n)
    		elif res.component.label == "Mod log [ON]":
    			n=C.json_open(f="log.json")
    			try:
    				await self.bot.wait_until_ready()
    				channel = discord.utils.get(ctx.guild.channels, name="mod-log")
    				await channel.delete()
    				n["mod"].remove(f"{ctx.guild.id}")
    				C.json_dump(f="log.json",n=n)
    				pass
    			except Exception as e:
    				await ctx.send(f"I can't delete the channel `Mod log` maybe i don't have perm or u have changed the channel name or ``` This is bcs bot can't delete young channel as its not save in cache``` SORRY!")
    				print(e)
    				pass
    		elif res.component.label == "Mod log [OFF]":
    			n=C.json_open(f="log.json")
    			n["mod"].append(f"{ctx.guild.id}")
    			try:
    			    guild = ctx.guild
    			    overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False),guild.me: discord.PermissionOverwrite(read_messages=True)}
    			    channel = await guild.create_text_channel('Mod log', overwrites=overwrites,topic="Don't change channel name warning! ! But u can change permissions")
    			    pass
    			except:
    				await ctx.send(f"sad i don't have perm to create channel")
    				pass
    			C.json_dump(f="log.json",n=n)
    		await res.respond(content = "For more info use .guide ",components=B.setup(ctx),type=7)
    #@
    
def setup(bot):
    bot.add_cog(button(bot))