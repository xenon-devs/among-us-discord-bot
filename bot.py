import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import time
import json
import os
import shutil
import asyncio
from discord.utils import get
import datetime
from discord import Spotify
from PIL import Image
from io import BytesIO
from PIL import ImageFont
from PIL import ImageDraw
from discord.ext import menus
import tenorpy
import pyfiglet
import dbl


class TopGG(commands.Cog):
    
	def __init__(self, bot):
		self.bot = bot
		self.token = os.environ.get('dbl_token')  # set this to your DBL token
		self.dblpy = dbl.DBLClient(self.bot, self.token)
		self.update_stats.start()

	def cog_unload(self):
		self.update_stats.cancel()

	@tasks.loop(minutes=30)
	async def update_stats(self):
		"""This function runs every 30 minutes to automatically update your server count."""
		await self.bot.wait_until_ready()
		try:
			server_count = len(self.bot.guilds)
			await self.dblpy.post_guild_count(server_count)
			print('Posted server count ({})'.format(server_count))
		except Exception as e:
			print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
		


def setup(bot):
    bot.add_cog(TopGG(bot))

# Testing if it works!


def get_prefix(client , message):
	main_server = client.get_guild(730075470694973461)
	# if len(main_server.text_channels) > 480:
	# 	main_server_2 = client.get_guild(753269919684231178)
	# 	for channel in main_server_2.text_channels:
	# 		if str(channel.name) == str(message.guild.id):
	# 			prfx = channel.topic
	# 			return prfx


	for channel in main_server.text_channels:
		try:
			if str(channel.name) == str(message.guild.id):
				prfx = channel.topic
				return prfx
		except AttributeError:
			return 'a!'

	basic_prefix = "a!"
	return basic_prefix

def get_count(client):
	count = 0
	for guild in client.guilds:
		count += guild.member_count

	return count

intents = discord.Intents(messages = True , guilds = True , reactions = True)
client = commands.Bot(command_prefix= get_prefix , intents = intents)
client.remove_command('help')
value = get_count(client)
status = cycle([f"{value} members" , f"{value} members"])

async def add_game(matchid , server , user , channel_to):
    with open('games.json' , 'r') as f:
        games = json.load(f)

    if str(user.id) in games:
        return await channel_to.send('You already have a Game running.')

    servers = ['asia' , 'europe' , 'na']

    if not server.lower() in servers:
        return await channel_to.send('Please specify a valid server among Asia , Europe and NA')

    games[str(user.id)] = {}
    games[str(user.id)]['id'] = matchid
    games[str(user.id)]['server'] = server

    with open('games.json', 'w') as f:
        json.dump(games , f)

    await channel_to.send('Your game added successfully!.')

async def fetch_available_games(channel_to , server:str = ''):
    with open('games.json' , 'r') as f:
        games = json.load(f)

    availableServers = ['asia' , 'europe' , 'na' , '']

    if not server.lower() in availableServers:
        return await channel_to.send('Invalid server name specified. Please choose one of Asia , Europe and NA')


    if len(games) == 0:
        return await channel_to.send('No games available right now. Please try again after some time.')

    string = ''
    correctServer = False
    for game in games:
        if server == '':
            string = string + '**Server** : ' + games[game]['server'] + ' , **id** : ' + games[game]['id'] + '\n'
            correctServer = True
        else:
            if games[game]['server'].lower() == server.lower():
                string = string + '**Server** : ' + games[game]['server'] + ' , **id** : ' + games[game]['id'] + '\n'
                correctServer = True

    if not correctServer:
        return await channel_to.send('No games available right now. Please try again')

    await channel_to.send(f'**Currently available Games**\n====================\n{string}\n====================')


async def remove_game(user):
    with open('games.json' , 'r') as f:
        games = json.load(f)

    del games[str(user.id)]

    with open('games.json' , 'w') as f:
        json.dump(games , f)

@client.command(aliases = ['Ascii' , 'ASCII'])
async def ascii(ctx , * , text = ''):
	await start_log("ascii")
	await update_log("ascii")
	if text == '':
		return await ctx.send('Please provide some text.')
	
	ascii_banner = pyfiglet.figlet_format(text)
	await ctx.send(f'```{ascii_banner}```')

@client.command(aliases = ["Prefix" , "PREFIX"])
async def prefix(ctx , prfx:str = ""):
	if not ctx.author.guild_permissions.manage_guild:
		await ctx.send("You do not have the necessary permissions")
		return
		
	if prfx == "":
		await ctx.send("Please specify a valid prefix")
		return
	else:
		main_server = client.get_guild(730075470694973461)
		for channel in main_server.text_channels:
			if channel.name == f"{ctx.guild.id}":
				await channel.edit(topic = prfx)
				await ctx.send(f"Your prefix changes successfully to {prfx}")
				return
		
		
		await main_server.create_text_channel(name = ctx.guild.id , topic = prfx)
		await ctx.send(f"Your prefix changes successfully to {prfx}")

# @client.event
# async def on_message(message):
# 	for member in message.mentions:
# 		if member == message.guild.me:
# 			embed = discord.Embed(title = "Bot details!!" , color = message.author.color)
# 			embed.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
# 			prfx = get_prefix(client = client , message = message)
# 			embed.add_field(name = "Among Us Unofficial#6602" , value = f"** **" , inline = False)
# 			embed.add_field(name = f"Current server prefix = {prfx}" , value = f"currently in {len(client.guilds)} servers" , inline = False)
# 			embed.add_field(name = f"For more information use {prfx}help" , value = "`Join the support server here` : [**Click Me**](https://discord.gg/tgyW2Jz)\n`To go to the official website` : [**Click Here**](https://amongusunofficial.godaddysites.com/)" , inline = False)
# 			embed.set_footer(text = "Bot developed by @Sammy Sins#6969" , icon_url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
# 			await message.channel.send(embed = embed)


# 	await client.process_commands(message)

@client.command(aliases = ['Host' , 'HOST'])
async def host(ctx , matchid:str = '' , server:str = ''):
	if matchid == '' or server == '':
		return await ctx.send('Please specify the Match ID and Server correctly')

	await add_game(matchid , server , ctx.author , ctx.channel)

	await asyncio.sleep(300)
	await remove_game(ctx.author)

# @client.command()
# async def push_update(ctx):
# 	embed = discord.Embed(title = "Among Us Bot update 2.0" ,description = "\n\n==============\n\nWe are very happy to announce the addition of some new features in the Bot.\nWith this update You can now play will all people of the Among Us community(believe me, there are a lot)\nYou can Host a game and also find matches using these new commands\nuse {prefix} help for more information`.Hope you enjoy the new feature.==============", color = discord.Color.orange())
# 	embed.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
# 	embed.set_footer(text = "With love. Among us team.")
# 	print('Pushing Update')
# 	for server in client.guilds:
# 		if not server.id == 110373943822540800:
# 			if server.system_channel is not None:
# 				try:
# 					await server.system_channel.send(embed = embed)
# 				except discord.Forbidden:
# 					pass
# 				else:
# 					print(f'Update pushed in {server.name}')
#
# 	print("Update pushed successfully")

@client.command(aliases = ['Match' , 'MATCH'])
async def match(ctx , server:str = ''):
	await fetch_available_games(ctx.channel , server)

@client.event
async def on_ready():
	change_status.start()
	setup(client)
	print("Bot is ready.")

@tasks.loop(minutes=15)
async def change_status():
	value = get_count(client)
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening , name = f"New Update. Use help command."))

@client.command(aliases = ["Emoji" , "EMOJI"])
async def emoji(ctx):
	await start_log("emoji")
	users = await get_log_data()
	await update_log("emoji")
	emojis = ["<:yes:759276088412471316>" , "<:why:759276133157044264>" , "<:whoIsImposter:759278022686670880>" , "<:whoareu:759275487222169600>" , "<:what:759276168679129108>",  "<:ruImposter:759275533023444992>" , "<:IsawUkilled:759275796816461834>" , "<:IdontKnow:759275922028757012>" , "<:idontkill:759275576480890880>" , "<:iamImposter:759275748778967070>" , "<:Hello:759276199406600244>" , "<:deadbody:759275974708690974>" , "<:dead:759276019303055360>" , "<:crewmate:759276054320775188>" , "<:letVoteOut:759275840948404266>"]
	emj = random.choice(emojis)
	await ctx.send(emj)

@client.command(aliases = ["RPS" , "Rps"])
async def rps(ctx):
	await start_log("1p")
	users = await get_log_data()
	await update_log("1p")
	await ctx.send("Play your move(rock/paper/scissors)")
	results = ["rock" , "paper" , "scissors"]
	def check(message):
		return message.author == ctx.author and message.channel == ctx.message.channel

	try:
		msg = await client.wait_for('message' , timeout = 30.0 , check = check)
	except asyncio.TimeoutError:
		await ctx.send("You took too long to play")
	else:
		answer = random.choice(results)
		if msg.content.lower() == "rock":
			if answer == "paper":
				await ctx.send("I chose paper and won!!, Better luck next time!")
			elif answer == "rock":
				await ctx.send("We both chose rock, Oof a TIE!!")
			elif answer == "scissors":
				await ctx.send("GG, You Won. Congratulations :partying_face:")
			else:
				await ctx.send("Please choose a valid option. Game Ended")
		elif msg.content.lower() == "paper":
			if answer == "scissors":
				await ctx.send("I chose Scissors and won!!, Better luck next time!")
			elif answer == "paper":
				await ctx.send("We both chose paper, Oof a TIE!!")
			elif answer == "rock":
				await ctx.send("GG, You Won. Congratulations :partying_face:")
			else:
				await ctx.send("Please choose a valid option. Game Ended")
		elif msg.content.lower() == "scissors":
			if answer == "rock":
				await ctx.send("I chose rock and won!!, Better luck next time!")
			elif answer == "scissors":
				await ctx.send("We both chose scissors, Oof a TIE!!")
			elif answer == "paper":
				await ctx.send("GG, You Won. Congratulations :partying_face:")
			else:
				await ctx.send("Please choose a valid option. Game Ended")
		else:
			await ctx.send("Please choose a valid option. Game Ended")

@client.command(aliases = ["Challenge" , "CHALLENGE"])
async def challenge(ctx , opponent:discord.Member):
	await start_log("2p")
	users = await get_log_data()
	await update_log("2p")

	if opponent == ctx.author:
		await ctx.send("You cannot play against yourself")
		return

	await ctx.send(f"{opponent.mention}, Do you accept the challenge?(yes/no)")
	def check(message):
		return message.channel == ctx.message.channel and message.author == opponent and message.content.lower() == 'yes' or message.content.lower() == 'no'

	try:
		msg = await client.wait_for('message' , timeout = 30.0 , check = check)
	except asyncio.TimeoutError:
		await ctx.send("You took too long to accept")
	else:
		if msg.content.lower() == "no":
			await ctx.send("Game ended")
			return
			
		await ctx.send("Get ready contestants, Check your dm")
		c1 = await ctx.author.create_dm()
		c2 = await opponent.create_dm()
		await ctx.author.dm_channel.send("Game starting in 5s")
		await opponent.dm_channel.send("Game starting in 5s")
		await asyncio.sleep(3)
		embed = discord.Embed(title = "Among Us Hand cricket!" , color = discord.Color.red())
		embed.set_image(url = "https://media.tenor.com/images/2ab9e2f21aece2154bc36bf6c9b2e09e/tenor.gif")
		embed.add_field(name = "Play your move(rock/paper/scissors)" , value = "** **")
		embedo = discord.Embed(title = "Among Us Hand cricket!" , color = discord.Color.blue())
		embedo.set_image(url = "https://media.tenor.com/images/d075fedb342564f3aefb67ff7895b953/tenor.gif")
		embedo.add_field(name = "Play your move(rock/paper/scissors)" , value = "** **")
		await ctx.author.dm_channel.send(embed = embed)
		await opponent.dm_channel.send(embed = embedo)
		def checka(message):
			return isinstance(message.channel, discord.channel.DMChannel) and message.author == ctx.author
		def checko(message):
			return isinstance(message.channel, discord.channel.DMChannel) and message.author == opponent
		try:
			msg = await client.wait_for('message' , timeout = 30.0 , check = checka)
			mtg = await client.wait_for('message' , timeout = 30.0 , check = checko)
			answer = mtg.content.lower()
		except asyncio.TimeoutError:
			await ctx.send("You took too long to respond")
		else:
			await c1.send(f"Your opponent chose {answer}")
			await c2.send(f"Your opponent chose {msg.content}")
			if msg.content.lower() == "rock":
				if answer == "paper":
					await c1.send("Better luck next time!")
					await c2.send("Congratulations:partying_face: You won!!")
					await ctx.send(f"{opponent.mention} Won against {ctx.author.mention}")
				elif answer == "rock":
					await c1.send("GG, You both tied")
					await c2.send("GG, You both tied")
					await ctx.send(f"{ctx.author.mention} and {opponent.mention} TIED!!")
				elif answer == "scissors":
					await c1.send("Congratulations:partying_face: You won!!")
					await c2.send("Better luck next time!")
					await ctx.send(f"{ctx.author.mention} Won against {opponent.mention}")
				else:
					await c2.send("Please choose a valid option. Game Ended")
			elif msg.content.lower() == "paper":
				if answer == "scissors":
					await c1.send("Better luck next time!")
					await c2.send("Congratulations:partying_face: You won!!")
					await ctx.send(f"{opponent.mention} Won against {ctx.author.mention}")
				elif answer == "paper":
					await c1.send("GG, You both tied")
					await c2.send("GG, You both tied")
					await ctx.send(f"{ctx.author.mention} and {opponent.mention} TIED!!")
				elif answer == "rock":
					await c1.send("Congratulations:partying_face: You won!!")
					await c2.send("Better luck next time!")
					await ctx.send(f"{ctx.author.mention} Won against {opponent.mention}")
				else:
					await c2.send("Please choose a valid option. Game Ended")
			elif msg.content.lower() == "scissors":
				if answer == "rock":
					await c1.send("Better luck next time!")
					await c2.send("Congratulations:partying_face: You won!!")
					await ctx.send(f"{opponent.mention} Won against {ctx.author.mention}")
				elif answer == "scissors":
					await c1.send("GG, You both tied")
					await c2.send("GG, You both tied")
					await ctx.send(f"{ctx.author.mention} and {opponent.mention} TIED!!")
				elif answer == "paper":
					await c1.send("Congratulations:partying_face: You won!!")
					await c2.send("Better luck next time!")
					await ctx.send(f"{ctx.author.mention} Won against {opponent.mention}")
				else:
					await c2.send("Please choose a valid option. Game Ended")
			else:
				await c1.send("Please choose a valid option. Game Ended")




@client.command(aliases = ["Coin_flip" , "COIN_FLIP" , "Flip_coin" , "flip_coin" , "FLIP_COIN" , "FLIP" , "Flip" , "coin_flip"])
async def flip(ctx):
	await start_log("coin_flip")
	users = await get_log_data()
	await update_log("coin_flip")
	embed = discord.Embed(title = f"{ctx.author.display_name} Has flipped a coin" , color = discord.Color.orange())
	embed.set_thumbnail(url = ctx.author.avatar_url)
	embed.set_image(url = "https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")
	links = ["https://media.tenor.com/images/d9cc74bec0a2a582d1887045c62595c9/tenor.gif" , "https://media.tenor.com/images/1de5555846dc3e3cd279983cbd2e986d/tenor.gif"]
	msg = await ctx.send(embed = embed)
	nembed = discord.Embed(title = f"And the result is ....." , color = discord.Color.orange())
	nembed.set_image(url = random.choice(links)) 
	await asyncio.sleep(8)
	await msg.edit(embed = nembed)


@client.command(aliases = ["Add_emoji" , "ADD_EMOJI" , "Add" , "add" , "ADD"])
async def add_emoji(ctx , name = None, number = 0):
	await start_log("add_emoji")
	users = await get_log_data()
	await update_log("add_emoji")
	emojis = ["<:yes:759276088412471316>" , "<:why:759276133157044264>" , "<:whoIsImposter:759278022686670880>" , "<:whoareu:759275487222169600>" , "<:what:759276168679129108>",  "<:ruImposter:759275533023444992>" , "<:IsawUkilled:759275796816461834>" , "<:IdontKnow:759275922028757012>" , "<:idontkill:759275576480890880>" , "<:iamImposter:759275748778967070>" , "<:Hello:759276199406600244>" , "<:deadbody:759275974708690974>" , "<:dead:759276019303055360>" , "<:crewmate:759276054320775188>" , "<:letVoteOut:759275840948404266>" , "<:me_ghost:763035423769100288>" , "<:shy_witch:763035032033165322>" , "<:doc_imposter:763035079706017832>" , "<:imposter:763035386585808916>" , "<:leave_me:763035256139022346>" , "<:announce:763035338842832897>" , "<:magician:763035212245368852>" , "<:not_me:763035139948281856>"]
	if name == None:
		embed = discord.Embed(title = "Emojis" , color = discord.Color.red())
		for i in range(len(emojis)):
			embed.add_field(name = "** **" , value = f"{i+1} : {emojis[i]}")

		embed.set_footer(text = "You need manage emojis permissions to use this" , icon_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS4HiptS4Q-kl6KMfBkVeJXTMqoVL4gO0rbaQ&usqp=CAU")

		await ctx.send(embed = embed)
		await ctx.send(f"Use add_emoji <name> <number> to add the emoji to your server Or add_emoji full-pack to add all emojis")
	
	elif name == "full-pack":
		if ctx.author.guild_permissions.manage_emojis:
			emojid = ["759276088412471316" , "759276133157044264" , "759278022686670880" , "759275487222169600" , "759276168679129108",  "759275533023444992" , "759275796816461834" , "759275922028757012" , "759275576480890880" , "759275748778967070" , "759276199406600244" , "759275974708690974" , "759276019303055360" , "759276054320775188" , "759275840948404266" , "763035423769100288" , "763035032033165322" , "763035079706017832" , "763035386585808916" , "763035256139022346" , "763035338842832897" , "763035212245368852" , "763035139948281856"]

			for emoji_id in emojid:
				emj = client.get_emoji(int(emoji_id))
				url = emj.url
				img = await url.read()
				emoji_name = emj.name
				await ctx.author.guild.create_custom_emoji(name = emoji_name , image = img)
			
			await ctx.send("Emojis successfully created")
		else:
			await ctx.send("You don't have the necessary permissions")
	else:
		if ctx.author.guild_permissions.manage_emojis:
			needed = number - 1
			emojid = ["759276088412471316" , "759276133157044264" , "759278022686670880" , "759275487222169600" , "759276168679129108",  "759275533023444992" , "759275796816461834" , "759275922028757012" , "759275576480890880" , "759275748778967070" , "759276199406600244" , "759275974708690974" , "759276019303055360" , "759276054320775188" , "759275840948404266" , "763035423769100288" , "763035032033165322" , "763035079706017832" , "763035386585808916" , "763035256139022346" , "763035338842832897" , "763035212245368852" , "763035139948281856"]
			emid = int(emojid[needed])
			emoji = client.get_emoji(emid)
			url = emoji.url
			img = await url.read()
			await ctx.author.guild.create_custom_emoji(name = name , image = img)
			await ctx.send("Emoji created")
		else:
			await ctx.send("You dont have the necessary permissions")



@client.command(aliases = ["Invite" , "INVITE"])
async def invite(ctx):
	await start_log("invite")
	users = await get_log_data()
	await update_log("invite")
	embed = discord.Embed(title = "Invite Among Us bot using the below link" , color = discord.Color.green())
	embed.add_field(name = "Go to the official server" , value = "[Click Me!](https://discord.gg/tgyW2Jz)")
	embed.add_field(name = "Invite the best Among Us Bot" , value = "[Invite](https://bit.ly/3ceYuEW)")
	embed.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
	await ctx.send(embed = embed)

@client.command(aliases = ["Report" , "REPORT"])
async def report(ctx, * ,problem = None):
	server = discord.utils.get(client.guilds , id = 757239002826014731)
	cnl = server.get_channel(763763201069940756)
	embed = discord.Embed(title = f"{ctx.author.display_name}'s Complaint/report" , color = discord.Color.orange())
	embed.add_field(name = "** **" , value = problem)
	await cnl.send(embed = embed)
	

@client.command(aliases = ["Vc" , "VC"])
async def vc(ctx , code = None , server = None):
	await start_log("vc")
	users = await get_log_data()
	await update_log("vc")
	if code == None:
		await ctx.send("Please enter the code of your Among Us game")
		msg = await client.wait_for('message' ,  check=lambda message: message.author == ctx.author)
		print(msg.content)
	if ctx.guild.id == 757239002826014731:
		cat = discord.utils.get(ctx.guild.categories , id = 757247392981450813)
	else:
		cat = ctx.message.channel.category

	await ctx.author.guild.create_voice_channel(name = f"🚀{code} -> {server}" , category = cat , user_limit = 11)
	vch = discord.utils.get(ctx.author.guild.voice_channels , name = f"🚀{code} -> {server}")
	vch.permissions_for(ctx.author)
	await ctx.author.create_dm()
	await ctx.author.dm_channel.send("Your voice channel has been created successfully, It will be deleted after 30 minutes. Here is your link.")
	link = await vch.create_invite(max_uses = 11)
	await ctx.author.dm_channel.send(f"{link}")
	await asyncio.sleep(1800)
	await vch.delete()

async def get_log_data():
	with open("logs.json" , "r") as f:
		users = json.load(f)

	return users

async def start_log(command_name):
	users = await get_log_data()

	if command_name in users:
		return False
	else:
		users[command_name] = {}
		users[command_name]["count"] = 0

	with open("logs.json" , "w") as f:
		json.dump(users,f)
	return True

async def update_log(command_name):
	users = await get_log_data()

	users[command_name]["count"] += 1

	with open("logs.json" , "w") as f:
		json.dump(users,f)

	bal = users[command_name]["count"]

	return bal

@client.command(aliases = ["Guess" , "GUESS"])
async def guess(ctx):
	embed = discord.Embed(title = "One of the below characters is an imposter, Let's see if you can spot it" , color = ctx.author.color)
	embed.set_image(url = "https://i.redd.it/7xvv3tmx8vo51.png")
	embed.set_footer(text = "Respond with your color, Let's see if you win!" , icon_url = "https://5droid.ru/uploads/posts/2020-02/1581588210_among-us.png")
	await ctx.send(embed = embed)
	colors = ["green" , "black" , "purple" , "blue" , "lime" , "white" , "pink" , "cyan" , "teal" , "yellow" , "red" , "brown" , "orange"]
	def check(message):
		return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in colors
	try:
		msg = await client.wait_for('message' , timeout = 30.0 , check = check)
	except asyncio.TimeoutError:
		await ctx.send("You took too long to respond. What a loser!!")
	else:
		ans2 = ""
		ans = random.choice(colors)
		if ans == "cyan" or ans == "teal":
			ans = "cyan"
			ans2 = "teal"
		if msg.content.lower() == ans or msg.content.lower() == ans2:
			await ctx.send(f":partying_face: You won!! GG :partying_face:")
		else:
			await ctx.send(f"{ans} was the imposter. Oof you missed it. Better luck next time")




# @client.command(aliases = ["Stats" , "STATS"])
# async def stats(ctx):
# 	users = await get_log_data()
# 	totalUsers  = get_count(client)
# 	c_count =  0
# 	for used in users:
# 		c_count += users[used]["count"]

# 	embed = discord.Embed(title="Among us Bot stats!",description=f"==============\n**Servers** : `{len(client.guilds)}`\n**Commands** : `{c_count}`\n**Users** : `{totalUsers}`\n==============", color=discord.Color.green())

# 	embed.set_thumbnail(url = "https://5droid.ru/uploads/posts/2020-02/1581588210_among-us.png")

# 	await ctx.send(embed = embed)

@client.command(aliases = ["Mute" , "MUTE"])
async def mute(ctx):
	await start_log("mute")
	users = await get_log_data()
	await update_log("mute")
	if ctx.author.voice.channel == None:
		await ctx.send("You have to be connected to a voice channel first")
		return

	await ctx.author.edit(mute = True)

	for member in ctx.author.voice.channel.members:
		if member.top_role < ctx.author.top_role:
			await member.edit(mute = True)

@client.command(aliases = ["Unmute" , "UNMUTE"])
async def unmute(ctx):
	await start_log("unmute")
	users = await get_log_data()
	await update_log("unmute")
	if ctx.author.voice.channel == None:
		await ctx.send("You have to be connected to a voice channel first")
		return

	await ctx.author.edit(mute = False)
		
	for member in ctx.author.voice.channel.members:
		if member.top_role < ctx.author.top_role:
			await member.edit(mute = False)



@client.command(aliases = ["Guide" , "GUIDE"])
async def guide(ctx):
	await start_log("guide")
	users = await get_log_data()
	await update_log("guide")
	embed = discord.Embed(title = "Among Us Guide Page" , color = discord.Color.orange())
	embed.set_image(url = "https://media.tenor.com/images/c3b4688a7189725f664c9c6af0b33003/tenor.gif")
	msg = await ctx.send(embed = embed)
	await asyncio.sleep(30)
	guide = discord.Embed(title = "Among Us Guide Page" , color = discord.Color.orange())
	guide.add_field(name = ":map:Full Guide" , value = "[Guide](https://bit.ly/2ZHsF2A)")
	guide.add_field(name = "<:among_us:769073995324063755>Crewmate" , value = "[Crewmate](https://bit.ly/3khxtU6)")
	guide.add_field(name = ":detective:Imposter" , value = "[Imposter](https://bit.ly/2ZHsF2A)")
	guide.add_field(name = "To learn about maps use the below command" , value = "a!maps" , inline = False)
	guide.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
	await msg.edit(embed = guide)

@client.command(aliases = ['Maps' , 'MAPS'])
async def maps(ctx):
	await start_log("maps")
	users = await get_log_data()
	await update_log("maps")
	prfx = get_prefix(client = client , message = ctx.message)
	among = discord.Embed(title = f"Choose one of the below maps by typing the command `{prfx}(map name)`.\n Eg. {prfx}skeld \nyou can choose between skeld, mirahq and polus" , color = discord.Color.orange())
	among.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
	await ctx.send(embed = among)
	
@client.command(aliases = ['Skeld' , 'SKELD'])
async def skeld(ctx):
	await start_log("skeld")
	users = await get_log_data()
	await update_log("skeld")
	skeld = discord.Embed(title = 'Skeld' , color = discord.Color.orange())
	skeld.set_image(url = 'https://preview.redd.it/tv8ef4iqszh41.png?auto=webp&s=46faf550020fd59c8d8bab29705b0fcb80521850')
	await ctx.send(embed = skeld)
	
@client.command(aliases = ['Polus' , 'POLUS'])
async def polus(ctx):
	await start_log("polus")
	users = await get_log_data()
	await update_log("polus")
	polus = discord.Embed(title = 'Polus' , color = discord.Color.orange())
	polus.set_image(url = 'https://vignette.wikia.nocookie.net/among-us-wiki/images/4/4c/Polus.png/revision/latest?cb=20200907133344')
	await ctx.send(embed = polus)
	
@client.command(aliases = ['Mirahq' , 'MIRAHQ'])
async def mirahq(ctx):
	await start_log("mirahq")
	users = await get_log_data()
	await update_log("mirahq")
	mira = discord.Embed(title = 'Mira HQ' , color = discord.Color.orange())
	mira.set_image(url = 'https://vignette.wikia.nocookie.net/among-us-wiki/images/0/0a/Mirahq.png/revision/latest?cb=20200907132939')
	await ctx.send(embed = mira)

@client.command(aliases = ["Kill" , "KILL" , "hit" , "Hit" , "HIT"])
async def kill(ctx , user:discord.Member = None):
	await start_log("kill")
	await update_log("kill")
	
	t = tenorpy.Tenor()
	if user == ctx.author:
		return await ctx.send('You cannot kill yourself, Please mention someone else.')
	else:
		# links = ["https://media.tenor.com/images/2ad01fc73cc91abd54069f2e8deb50cc/tenor.gif","https://media.tenor.com/images/49f4a71df065a3bf90d9ebfd0cbd2d58/tenor.gif" , "https://media.tenor.com/images/091a8ed3a3896e8f3b4bffa02c298491/tenor.gif" , "https://media.tenor.com/images/f2295524300b47930f650f82080e0bb5/tenor.gif" ,"https://media.tenor.com/images/a461243877f3e2494a4c69999b232a97/tenor.gif" ,"https://media.tenor.com/images/7bb1baedb25f70d66d811088e464c4a3/tenor.gif" ,"https://media.tenor.com/images/d46c724d422714d738a84a51f1caf00b/tenor.gif" , "https://media.tenor.com/images/a166604b0b8f34779dbbd2dd690efb58/tenor.gif"]
		lnk = t.search(tag = "among us kill" , limit = 20)
		link_start = random.choice(lnk['results'])
		link = link_start['media'][0]['gif']['url']
		lit = f"{ctx.author.display_name} Killed {user.display_name}"
	embed = discord.Embed(title = lit , color = discord.Color.red())
	embed.set_image(url = link)
	await ctx.send(embed = embed)

@client.command(aliases = ["Ping" , "PING"])
async def ping(ctx):
	await start_log("ping")
	users = await get_log_data()
	await update_log("ping")
	await ctx.send(f'Ping: {round(client.latency * 1000)} ms')


# @client.event
# async def on_guild_join(guild):
# 	cnl = client.get_channel(759265178616332308)
# 	await cnl.send(f"Among Us bot was added to {guild.name}")
# 	embed = discord.Embed(title="Bot details!!", color=discord.Color.orange())
# 	embed.set_thumbnail(url="https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
# 	prfx = 'a!'
# 	embed.add_field(name="Among Us Unofficial#6602", value=f"** **", inline=False)
# 	embed.add_field(name=f"Current server prefix = {prfx}", value=f"currently in {len(client.guilds)} servers",inline=False)
# 	embed.add_field(name=f"For more information use {prfx}help",value="Join the support server here: [**Click Me**](https://discord.gg/tgyW2Jz)", inline=False)
# 	embed.set_footer(text="Bot developed by @Sammy Sins#7295",icon_url="https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
# 	await guild.system_channel.send(embed = embed)

@client.command(aliases = ["Imposter" , "IMPOSTER" , "im" , "Im" , "IM"])
async def imposter(ctx , user : discord.Member = None):
	await start_log("imposter")
	users = await get_log_data()
	await update_log("imposter")


	if user == None:
		user = ctx.author

	impost = Image.open("imposter.jpg")

	asset = user.avatar_url_as(format = 'jpg' , size = 1024)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((177 , 177))

	impost.paste(pfp , (225 , 176))

	impost.save("profile.jpg")


	await ctx.send(file = discord.File("profile.jpg"))

@client.command(aliases = ["Crewmate" , "CREWMATE" , "cm" , "Cm" , "CM"])
async def crewmate(ctx , user : discord.Member = None):
	await start_log("crewmate")
	users = await get_log_data()
	await update_log("crewmate")


	if user == None:
		user = ctx.author

	impost = Image.open("crewmate.png")

	asset = user.avatar_url_as(format = 'png' , size = 1024)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)

	pfp = pfp.resize((181 , 181))

	impost.paste(pfp , (529 , 431))

	impost.save("profile.png")


	await ctx.send(file = discord.File("profile.png"))

class testing(menus.Menu):
	def __init__(self):
		super().__init__(timeout=90.0 , delete_message_after=True)

	async def send_initial_message(self , ctx ,channel):
		start = discord.Embed(title = 'Among Us Help' , description = 'React below to pick an option\n:radioactive: ➜ Among Us Utilities\n:game_die: ➜ Fun & Games\n:clipboard: ➜ Utilities\n`Liked the bot? To vote it` : **[Click here](https://top.gg/bot/757272442820362281/vote)**\n`To join support server` : [Click Here](https://discord.gg/tgyW2Jz)\n`To go to bots website` : [Click Here](https://amongusunofficial.godaddysites.com/)\n`To browse through bots code` : [Click Here](https://github.com/Cooldude069/AmongUs.git)' , color = discord.Color.orange())
		start.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
		start.set_footer(text = f'Command ran by {self.ctx.author.display_name}')

		return await channel.send(embed = start)

	@menus.button('☢')
	async def amngutils(self , payload):
		p = get_prefix(client = client , message = self.message)
		au = discord.Embed(title = '☢ Among us Utilities' , description = f'`{p}guide` ➜ Will teach you to play\n`{p}maps` ➜ Will show you the blueprints of all maps\n`{p}vc <code> <server>` ➜ Will create a voice channel\n`{p}mute` ➜ Mutes people lower than you in the vc\n`{p}unmute` ➜ Unmutes people lower than you in the vc\n`{p}host <Code> <Server>` ➜ Makes your game discoverable to others\n`{p}match <server>` ➜ Shows you the visible games in that server' , color = discord.Color.orange())
		au.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
		au.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
		await self.message.edit(embed = au)

	@menus.button('🎲')
	async def fng(self , payload):
		p = get_prefix(client = client , message = self.message)
		f = discord.Embed(title = '🎲 Fun & Games' , description = f'`{p}rps` ➜ Starts a rock, paper , scissors game with the bot\n`{p}challenge <user>` ➜ Play a 1v1 rock, paper scissors with your friend\n`{p}flip` ➜ Flips a coin for you\n`{p}kill <user>` ➜ Sends a cool among us killing gif\n`{p}imposter <user>` ➜ makes him/her an Imposter\n`{p}crewmate <user>` ➜ makes him/her a Crewmate\n`{p}guess` ➜ You have to guess the imposter\n`{p}ascii <text>` ➜ Creates an ASCII banner of that text' , color = discord.Color.orange())
		f.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
		f.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
		await self.message.edit(embed = f)

	@menus.button('📋')
	async def utils(self , payload):
		p = get_prefix(client = client , message = self.message)
		u = discord.Embed(title = '📋 Utilities' , description = f'`{p}emoji` ➜ Generates a random Among Us emoji\n`{p}add` ➜ Adds emojis to your server\n`{p}ping` ➜ displays the bots latency\n`{p}prefix <new prefix>` ➜ Changes the bots prefix' , color = discord.Color.orange())
		u.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
		u.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
		await self.message.edit(embed = u)

	@menus.button('🏠')
	async def home(self , payload):
		start = discord.Embed(title = 'Among Us Help' , description = 'React below to pick an option\n:radioactive: ➜ Among Us Utilities\n:game_die: ➜ Fun & Games\n:clipboard: ➜ Utilities\n`Liked the bot? To vote it` : **[Click here](https://top.gg/bot/757272442820362281/vote)**\n`To join support server` : [Click Here](https://discord.gg/tgyW2Jz)\n`To go to bots website` : [Click Here](https://amongusunofficial.godaddysites.com/)\n`To browse through bots code` : [Click Here](https://github.com/Cooldude069/AmongUs.git)' , color = discord.Color.orange())
		start.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
		start.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
		await self.message.edit(embed = start)

	# @menus.button('🏏')
	# async def crick(self , payload):
	# 	hc = discord.Embed(title = 'Introducing Hand Cricketer bot' , description = "**Wanna play Cricket on Discord with your friends?**\nDon't worry, we got you covered.Invite the new handcricketer bot and play cricket with your friends all day long via Discord.\n=========================\nBot Invite Link : [Click Here](https://top.gg/bot/709733907053936712)\n=========================\n" , color = discord.Color.darker_grey())
	# 	hc.set_footer(text = "To Advertise your discord bot/server, join the support server.")
	# 	hc.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/709733907053936712/0670b3d504ecbe6c4871c6301bf68cea.webp')
	# 	await self.message.edit(embed = hc)


class helper(menus.Menu):
	global i
	i = 0

	def __init__(self):
		super().__init__(timeout = 30.0 , delete_message_after = False)


	async def send_initial_message(self , ctx , channel):
		prfx = get_prefix(client = client , message = self.ctx.message)
		embed0 = discord.Embed(title = "Among Us help!" , description = f"Hey!, I am the Among us Bot!, I do some cool things(that's why i am the best)\nMy prefix is {prfx}, So let's go through my commands!\n\n==============\n\n<:deadbody:759275974708690974> **Page 2** : `Among us utilities`\n\n<:reddit:314349923103670272> **Page 3** : `Fun commands`\n\n<:staff:314068430787706880> **Page 4** : `General utilities`\n\n:cricket_game: **Page 5** : `Hand Cricket Bot`\n\n`To join the support server` : [**Click Here**](https://discord.gg/pzxhrJ4UHV)\n`To go to the official website` : [**Click Here**](https://amongusunofficial.godaddysites.com/)\n\n==============" , color = discord.Color.orange())
		embed0.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")	
		embed0.set_footer(text = "Use the below reactions to navigate")	
		global i
		i = 1

		return await channel.send(embed = embed0)

	@menus.button('⏮')
	async def on_begin(self , payload):
		global i
		prfx = get_prefix(client = client , message = self.ctx.message)
		embed0 = discord.Embed(title = "Among Us help!" , description = f"Hey!, I am the Among us Bot!, I do some cool things(that's why i am the best)\nMy prefix is {prfx}, So let's go through my commands!\n\n==============\n\n<:deadbody:759275974708690974> **Page 2** : `Among us utilities`\n\n<:reddit:314349923103670272> **Page 3** : `Fun commands`\n\n<:staff:314068430787706880> **Page 4** : `General utilities`\n\n:cricket_game: **Page 5** : `Hand Cricket Bot`\n\n`To join the support server` : [**Click Here**](https://discord.gg/pzxhrJ4UHV)\n`To go to the official website` : [**Click Here**](https://amongusunofficial.godaddysites.com/)\n\n==============" , color = discord.Color.orange())
		embed0.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
		embed0.set_footer(text = "use the below reactions to navigate")
		await self.message.edit(embed = embed0)
		i = 1

	@menus.button('⏪')
	async def on_rewind(self , payload):
		global i
		if i == 3:
			helpm2  = discord.Embed(title = f"Among Us Help! Page {i - 1}" , color = discord.Color.darker_grey())
			helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
			helpm2.add_field(name = ":one: guide -> will guide you" , value = "This will give you all the required information about the game" , inline = False)
			helpm2.add_field(name = ":two: maps -> will show you all maps" , value = "This will give you the blueprints of all the maps" , inline = False)
			helpm2.add_field(name = ":three: vc {code} {server} -> Makes a special voice channel" , value = "U can invite the people you want(limit = 11)" , inline = False)
			helpm2.add_field(name = ":four: mute -> Mutes the people in the voice channel" , value = "Only the people who have a role lower than you will be muted" , inline = False)
			helpm2.add_field(name = ":five: unmute -> Unmutes the people in the voice channel" , value = "Keep the discussions going" , inline = False)
			helpm2.add_field(name = ":fire::fire:New Features :fire::fire:" , value = "** **" , inline = False)
			helpm2.add_field(name = ":six: host {Code} {Server} -> Hosts a Game which is available to the Entire community." , value = "Yous game will be erased after 60s" , inline = False)
			helpm2.add_field(name = ":seven: match {server} -> Shows all the available games in that server which have been Hosted" , value = "If server not specified, It will search globally.Servers -> Asia , Europe , NA" , inline = False)
			await self.message.edit(embed = helpm2)
			i = i - 1
		elif i == 4:
			helpm2  = discord.Embed(title = f"Among Us Help! Page {i - 1}" , color = discord.Color.darker_grey())
			helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
			helpm2.add_field(name = ":one: rps -> Starts a rock, paper , scissors game with the bot" , value = "It is really fun" , inline = False)
			helpm2.add_field(name = ":two: challenge {user} -> Play a 1v1 rock, paper scissors with your friend" , value = "It takes place in Dm, Don't worry" , inline = False)
			helpm2.add_field(name = ":three: flip -> Flips a coin for you" , value = "Solve your disputes with just a flip of the coin" , inline = False)
			helpm2.add_field(name = ":four: kill/hit {user} -> Just a fun command" , value = "try it, it's epic" , inline = False)
			helpm2.add_field(name = ":five: imposter/im {user} -> makes an Among Us imposter screen of that user" , value = "Please dont kick him out!" , inline = False)
			helpm2.add_field(name = ":six: guess -> creates a guessing game where you have to guess the imposter" , value = "Hmmm, fascinating!" , inline = False)
			helpm2.add_field(name = ':seven: ascii {text} -> creates an ascii banner of thaat text.' , value = 'ASCII is dope.' , inline = False)
			await self.message.edit(embed = helpm2)
			i = i - 1
		elif i == 2:
			embed0 = discord.Embed(title = "Among Us help!" , description = "Hey!, I am the Among us Bot!, I do some cool things(that's why i am the best)\nMy prefix is a!, So let's go through my commands!\n\n==============\n\n<:deadbody:759275974708690974> **Page 2** : `Among us utilities`\n\n<:reddit:314349923103670272> **Page 3** : `Fun commands`\n\n<:staff:314068430787706880> **Page 4** : `General utilities`\n\n:cricket_game: **Page 5** : `Hand Cricket Bot`\n\n`To join the support server` : [**Click Here**](https://discord.gg/pzxhrJ4UHV)\n`To go to the official website` : [**Click Here**](https://amongusunofficial.godaddysites.com/)\n\n==============" , color = discord.Color.orange())
			embed0.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
			i = i - 1
			await self.message.edit(embed = embed0)
		elif i == 5:
			prfx = get_prefix(client = client , message = self.ctx.message)
			helpm2 = discord.Embed(title = f"Among Us Help! Page {i - 1}" , color = discord.Color.darker_grey())
			helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
			helpm2.add_field(name = ":one: emoji -> Generates a random Among Us emoji" , value = "I love those Emoji's" , inline = False)
			helpm2.add_field(name = ":two: add_emoji/add -> adds the among us emoji to your server" , value = f"use {prfx}add to know how to go forward" , inline = False)
			helpm2.add_field(name = ":three: ping -> Shows the bot's latency" , value = "Pong!" , inline = False)
			helpm2.add_field(name = ":four: prefix {new prefix} -> to change the bot's prefix" , value = "The default prefix of the bot is a!" , inline = False)
			await self.message.edit(embed = helpm2)
			i = i - 1

	@menus.button('⏯')
	async def on_stop(self, payload):
		self.stop()

	@menus.button('⏩')
	async def on_skip(self , payload):
		global i
		if i == 1:
			helpm2  = discord.Embed(title = f"Among Us Help! Page {i + 1}" , color = discord.Color.darker_grey())
			helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
			helpm2.add_field(name = ":one: guide -> will guide you" , value = "This will give you all the required information about the game" , inline = False)
			helpm2.add_field(name = ":two: maps -> will show you all maps" , value = "This will give you the blueprints of all the maps" , inline = False)
			helpm2.add_field(name = ":three: vc {code} {server} -> Makes a special voice channel" , value = "U can invite the people you want(limit = 11)" , inline = False)
			helpm2.add_field(name = ":four: mute -> Mutes the people in the voice channel" , value = "Only the people who have a role lower than you will be muted" , inline = False)
			helpm2.add_field(name = ":five: unmute -> Unmutes the people in the voice channel" , value = "Keep the discussions going" , inline = False)
			helpm2.add_field(name=":fire::fire:New Features :fire::fire:", value="** **", inline=False)
			helpm2.add_field(
				name=":six: host {Code} {Server} -> Hosts a Game which is available to the Entire community.",
				value="Yous game will be erased after 60s", inline=False)
			helpm2.add_field(
				name=":seven: match {server} -> Shows all the available games in that server which have been Hosted",
				value="If server not specified, It will search globally.Servers -> Asia , Europe , NA", inline=False)
			await self.message.edit(embed = helpm2)
			i+=1
		elif i == 2:
			helpm2  = discord.Embed(title = f"Among Us Help! Page {i + 1}" , color = discord.Color.darker_grey())
			helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
			helpm2.add_field(name = ":one: rps -> Starts a rock, paper , scissors game with the bot" , value = "It is really fun" , inline = False)
			helpm2.add_field(name = ":two: challenge {user} -> Play a 1v1 rock, paper scissors with your friend" , value = "It takes place in Dm, Don't worry" , inline = False)
			helpm2.add_field(name = ":three: flip -> Flips a coin for you" , value = "Solve your disputes with just a flip of the coin" , inline = False)
			helpm2.add_field(name = ":four: kill/hit {user} -> Just a fun command" , value = "try it, it's epic" , inline = False)
			helpm2.add_field(name = ":five: imposter/im {user} -> makes an Among Us imposter screen of that user" , value = "Please dont kick him out!" , inline = False)
			helpm2.add_field(name = ":six: guess -> creates a guessing game where you have to guess the imposter" , value = "Hmmm, fascinating!" , inline = False)
			helpm2.add_field(name = ':seven: ascii {text} -> creates an ascii banner of thaat text.' , value = 'ASCII is dope.' , inline = False)
			await self.message.edit(embed = helpm2)
			i+=1
		elif i == 3:
			prfx = get_prefix(client = client , message = self.ctx.message)
			helpm2  = discord.Embed(title = f"Among Us Help! Page {i + 1}" , color = discord.Color.darker_grey())
			helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
			helpm2.add_field(name = ":one: emoji -> Generates a random Among Us emoji" , value = "I love those Emoji's" , inline = False)
			helpm2.add_field(name = ":two: add_emoji/add -> adds the among us emoji to your server" , value = f"use {prfx}add to know how to go forward" , inline = False)
			helpm2.add_field(name = ":three: ping -> Shows the bot's latency" , value = "Pong!" , inline = False)
			helpm2.add_field(name = ":four: prefix {new prefix} -> to change the bot's prefix" , value = "The default prefix of the bot is a!" , inline = False)
			await self.message.edit(embed = helpm2)
			i+=1
		elif i == 4:
			hc = discord.Embed(title = 'Introducing Hand Cricketer bot' , description = "**Wanna play Cricket on Discord with your friends?**\nDon't worry, we got you covered.Invite the new handcricketer bot and play cricket with your friends all day long via Discord.\n=========================\nBot Invite Link : [Click Here](https://top.gg/bot/709733907053936712)\n=========================\n" , color = discord.Color.darker_grey())
			hc.set_footer(text = "To Advertise your discord bot/server, join the support server.")
			hc.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/709733907053936712/0670b3d504ecbe6c4871c6301bf68cea.webp')
			await self.message.edit(embed = hc)

		
	@menus.button('⏭')
	async def on_end(self, payload):
		global i
		# prfx = get_prefix(client = client , message = self.ctx.message)
		# helpm2  = discord.Embed(title = f"Among Us Help! Page 4" , color = discord.Color.darker_grey())
		# helpm2.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
		# helpm2.add_field(name = ":one: emoji -> Generates a random Among Us emoji" , value = "I love those Emoji's" , inline = False)
		# helpm2.add_field(name = ":two: add_emoji/add -> adds the among us emoji to your server" , value = f"use {prfx}add to know how to go forward" , inline = False)
		# helpm2.add_field(name = ":three: ping -> Shows the bot's latency" , value = "Pong!" , inline = False)
		# helpm2.add_field(name = ":four: prefix {new prefix} -> to change the bot's prefix" , value = "The default prefix of the bot is a!" , inline = False)
		# await self.message.edit(embed = helpm2)
		hc = discord.Embed(title = 'Introducing Hand Cricketer bot' , description = "**Wanna play Cricket on Discord with your friends?**\nDon't worry, we got you covered.Invite the new handcricketer bot and play cricket with your friends all day long via Discord.\n=========================\nBot Invite Link : [Click Here](https://top.gg/bot/709733907053936712)\n=========================\n" , color = discord.Color.darker_grey())
		hc.set_footer(text = "To Advertise your discord bot/server, join the support server.")
		hc.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/709733907053936712/0670b3d504ecbe6c4871c6301bf68cea.webp')
		await self.message.edit(embed = hc)
		i = 5


# @client.command(aliases=['HELP', 'Help'])
# async def help(ctx):
# 	await start_log("help")
# 	users = await get_log_data()
# 	await update_log("help")
# 	m = testing()
# 	await m.start(ctx)



client.load_extension('memes')
TOKEN = os.environ.get('discord_bot_token')
client.run(TOKEN)
