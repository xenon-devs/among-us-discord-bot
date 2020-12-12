import discord
from discord.ext import commands
import praw
import random
from PIL import Image , ImageDraw , ImageFont
import dbl
import os
from discord.ext import menus
from io import BytesIO
import json


def get_prefix(client , message):
	main_server = client.get_guild(730075470694973461)
	if len(main_server.text_channels) > 480:
		main_server_2 = client.get_guild(753269919684231178)
		for channel in main_server_2.text_channels:
			if str(channel.name) == str(message.guild.id):
				prfx = channel.topic
				return prfx


	for channel in main_server.text_channels:
		if str(channel.name) == str(message.guild.id):
			prfx = channel.topic
			return prfx

	basic_prefix = "a!"
	return basic_prefix

def get_count(client):
	count = 0
	for guild in client.guilds:
		count += guild.member_count

	return count

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

class Helpfunc(menus.Menu):
    def __init__(self , client):
        self.client = client
        self.token = os.environ.get('dbl_token')
        self.dblpy = dbl.DBLClient(client , self.token)
        super().__init__(timeout=90.0 , delete_message_after=True)

    async def send_initial_message(self , ctx ,channel):
        start = discord.Embed(title = 'Among Us Help' , description = 'React below to pick an option\n:radioactive: ➜ Among Us Utilities\n:game_die: ➜ Fun & Games\n:clipboard: ➜ Utilities\n🤩 ➜ Memes\n`Liked the bot? To vote it` : **[Click here](https://top.gg/bot/757272442820362281/vote)**\n`To join support server` : [Click Here](https://discord.gg/tgyW2Jz)\n`To go to bots website` : [Click Here](https://amongusunofficial.godaddysites.com/)\n`To browse through bots code` : [Click Here](https://github.com/Cooldude069/AmongUs.git)' , color = discord.Color.orange())
        start.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
        start.set_footer(text = f'Command ran by {self.ctx.author.display_name}')

        return await channel.send(embed = start)

    @menus.button('☢')
    async def amngutils(self , payload):
        p = get_prefix(self.client , self.message)
        au = discord.Embed(title = '☢ Among us Utilities' , description = f'`{p}guide` ➜ Will teach you to play\n`{p}maps` ➜ Will show you the blueprints of all maps\n`{p}vc <code> <server>` ➜ Will create a voice channel\n`{p}mute` ➜ Mutes people lower than you in the vc\n`{p}unmute` ➜ Unmutes people lower than you in the vc\n`{p}host <Code> <Server>` ➜ Makes your game discoverable to others\n`{p}match <server>` ➜ Shows you the visible games in that server' , color = discord.Color.orange())
        au.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
        au.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
        await self.message.edit(embed = au)

    @menus.button('🎲')
    async def fng(self , payload):
        p = get_prefix(self.client , self.message)
        f = discord.Embed(title = '🎲 Fun & Games' , description = f'`{p}rps` ➜ Starts a rock, paper , scissors game with the bot\n`{p}challenge <user>` ➜ Play a 1v1 rock, paper scissors with your friend\n`{p}flip` ➜ Flips a coin for you\n`{p}kill <user>` ➜ Sends a cool among us killing gif\n`{p}imposter <user>` ➜ makes him/her an Imposter\n`{p}crewmate <user>` ➜ makes him/her a Crewmate\n`{p}guess` ➜ You have to guess the imposter\n`{p}ascii <text>` ➜ Creates an ASCII banner of that text' , color = discord.Color.orange())
        f.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
        f.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
        await self.message.edit(embed = f)

    @menus.button('📋')
    async def utils(self , payload):
        p = get_prefix(self.client , self.message)
        u = discord.Embed(title = '📋 Utilities' , description = f'`{p}emoji` ➜ Generates a random Among Us emoji\n`{p}add` ➜ Adds emojis to your server\n`{p}ping` ➜ displays the bots latency\n`{p}prefix <new prefix>` ➜ Changes the bots prefix' , color = discord.Color.orange())
        u.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
        u.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
        await self.message.edit(embed = u)

    @menus.button('🤩')
    async def mc(self , payload):
        p = get_prefix(self.client , self.message)
        voted = await self.dblpy.get_user_vote(self.ctx.author.id)
        if voted:
            description = f'`{p}meme` ➜ Fetches a funny meme from Reddit\n`{p}drake <text> , <text>` ➜ Generates a Drake meme\n`{p}sword <text> , <text>`➜ Generates a Sword meme\n`{p}announce <text>` ➜ Generates a Simpson meme.\n`{p}patrick <text>` ➜ Generates a Patrick meme\n`{p}spongebob <text>` ➜ Generates a Spongebob meme\n`{p}shit <text>` ➜ Generates a stepped-in-shit meme\n`{p}santa <text>` ➜ Generates a Santa meme\n`{p}fbi <text>` ➜ Generates an FBI meme\n`{p}slap <user>` ➜ slapping others is fun\n`{p}armor <text>` ➜ Generates an Armor meme\n`{p}monster <text>` ➜ Generates a Monster meme\n'
        else:
            description = '''```
        .--------.
       / .------. \ 
      / /        \ \ 
      | |        | |
     _| |________| |_
    .'|_|        |_| '.
    '._____ ____ _____.'
    |     .'____'.     |
    '.__.'.'    '.'.__.'
    '.__  |      |  __.'
    |   '.'.____.'.'   |
    '.____'.____.'____.'
    '.________________.'```\nUpvote the Bot to access this category.\n`To upvote the Bot ` **[Click Here](https://top.gg/bot/757272442820362281/vote)**'''
                                            
        m = discord.Embed(title = '🤩 Memes' , description = description , color = discord.Color.orange())
        m.set_thumbnail(url = 'https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO')
        m.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
        await self.message.edit(embed = m)

    @menus.button('🏠')
    async def home(self , payload):
        start = discord.Embed(title = 'Among Us Help' , description = 'React below to pick an option\n:radioactive: ➜ Among Us Utilities\n:game_die: ➜ Fun & Games\n:clipboard: ➜ Utilities\n🤩 ➜ Memes\n`Liked the bot? To vote it` : **[Click here](https://top.gg/bot/757272442820362281/vote)**\n`To join support server` : [Click Here](https://discord.gg/tgyW2Jz)\n`To go to bots website` : [Click Here](https://amongusunofficial.godaddysites.com/)\n`To browse through bots code` : [Click Here](https://github.com/Cooldude069/AmongUs.git)' , color = discord.Color.orange())
        start.set_thumbnail(url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO")
        start.set_footer(text = f'Command ran by {self.ctx.author.display_name}')
        await self.message.edit(embed = start)

class Memes(commands.Cog):
    def __init__(self , client):
        self.client = client
        self.token = os.environ.get('dbl_token')
        self.dblpy = dbl.DBLClient(self.client , self.token)

    @commands.Cog.listener()
    async def on_user_vote(self , data):
        user_id = int(data['user'])
        user = self.client.get_user(user_id)
        channel = self.client.get_channel(785782444594036747)
        await channel.send(f'{user.name} Just voted Among Us bot.')

    @commands.command(aliases = ['Meme' , 'MEME'])
    async def meme(self , ctx):
        await start_log("meme")
        await update_log("meme")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        reddit = praw.Reddit(client_id = '0bD1UHrRzjDbGQ',
                            client_secret = '9xoApJv0eZeRr1QVGJJulIE5cjXyFg',
                            username = 'CooLDuDE-6_9',
                            password = 'samarth1709',
                            user_agent = 'AmongUsUnofficial')

        memeList = []

        dankmemes = reddit.subreddit('dankmemes')
        hot = dankmemes.hot(limit = 50)
        for meme in hot:
            memeList.append(meme)

        rmemes = reddit.subreddit('memes')
        mHot = rmemes.hot(limit = 50)
        for nmeme in mHot:
            memeList.append(nmeme)

        sendable_meme = random.choice(memeList)
        embed = discord.Embed(description = f'**[{sendable_meme.title}]({sendable_meme.url})**' , color = discord.Color.from_rgb(random.randint(0 , 255), random.randint(0 , 255) ,random.randint(0 , 255)))
        embed.set_image(url = sendable_meme.url)
        embed.set_footer(text = f'🔥 {sendable_meme.score} | 💬 {len(sendable_meme.comments)}')
        await ctx.send(embed = embed)

    @commands.command(aliases = ['Monster' , 'MONSTER'])
    async def monster(self , ctx , * , text = ''):
        await start_log("monster")
        await update_log("monster")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        if len(text) > 60:
            return await ctx.send('Your text cannot exceed 60 characters')
        img = Image.open('monster.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf' , 20)
        increment = 0
        if len(text) > 30:
            txt = ''
            while len(text) > 30:
                txt = text[0:29]
                draw.text((45,370+increment) , txt , (0,0,0) , font = font)
                increment += 40
                text = text[29:]

            draw.text((45,370+increment) , text , (0,0,0) , font = font)
        else:
            draw.text((45,370) , text , (0,0,0) , font = font)

        img.save('monsterout.jpg')
        await ctx.send(file = discord.File('monsterout.jpg'))


    @commands.command(aliases = ['Drake' , 'DRAKE'])
    async def drake(self , ctx , * , text = ''):
        await start_log("drake")
        await update_log("drake")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text separated by a ","')

        index = text.find(',')
        if index == -1:
            return await ctx.send('You need to pass some text separated by a ","')

        text_one , text_two = text.split(',')

        if len(text_one) > 42 or len(text_two) > 42:
            return await ctx.send('Your text cannot exceed 48 characters(total of 84 including both).')

        img = Image.open('drake.jpg')
        draw = ImageDraw.Draw(img)
        t_one = text_one
        t_two = text_two
        font = ImageFont.truetype('arial.ttf' , 60)
        increment = 0
        if len(t_one) > 14:
            while len(text_one) > 14:
                t_one = text_one[0:13]
                draw.text((520 , 40 + increment) , t_one , (0 , 0, 0),font = font)
                increment += 130
                text_one = text_one[13:]

            draw.text((520 , 40 + increment) , text_one , (0 , 0, 0),font = font)
        else:
            draw.text((520 , 40) , t_one , (0 , 0, 0),font = font)

        increment = 0 
        if len(text_two) > 14:
            while len(text_two) > 14:
                t_two = text_two[0:13]
                draw.text((520 , 460 + increment) , t_two , (0 , 0, 0),font = font)
                increment += 130
                text_two = text_two[13:]
            
            draw.text((520 , 460 + increment) , text_two , (0 , 0, 0),font = font)
        else:
            draw.text((520 , 460) , t_two , (0 , 0, 0),font = font)

        img.save('drakeout.jpg')
        await ctx.send(file = discord.File('drakeout.jpg'))

    @commands.command(aliases = ['Sword' , 'SWORD'])
    async def sword(self , ctx , *,text = ''):
        await start_log("sword")
        await update_log("sword")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)
            
        if text == '':
            return await ctx.send('You have to provide two texts separated by a ","')

        index = text.find(',')

        if index == -1:
            return await ctx.send('You have to provide two texts separated by a ","')

        # 132,73 font = 40

        # 11 , 12

        text_one , text_two = text.split(',')
        if len(text_one) > 10 or len(text_two) > 20:
            return await ctx.send('The first text should not exceed 11 characters and second cannot exceed 21.')

        img = Image.open('sword.jfif')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf' , 40)
        draw.text((132,73) , text_one , (0,0,0) , font = font)
        draw.text((68,273) , text_two , (0,0,0) , font = font)

        img.save('swordout.jpg')
        await ctx.send(file = discord.File('swordout.jpg'))

    @commands.command(aliases = ['Announce' , 'ANNOUNCE'])
    async def announce(self , ctx , * , text = ''):
        await start_log("announce")
        await update_log("announce")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        if len(text) > 78:
            return await ctx.send('Your text cannot exceed 78 characters.')

        font = ImageFont.truetype('arial.ttf' , 60)
        img = Image.open('announce.png')
        draw = ImageDraw.Draw(img)
        #450 , 80
        #450 , 225
        increment = 0
        if len(text) > 26:
            txt = ''
            while len(text) > 26:
                txt = text[0:25]
                draw.text((450 , 80+increment) , txt , (0,0,0) , font = font)
                increment += 145
                text = text[25:]

            draw.text((450 , 80+increment) , text , (0,0,0) , font = font)
        else:
            draw.text((450 , 80) , text , (0,0,0) , font = font)

        img.save('announceout.png')
        await ctx.send(file = discord.File('announceout.png'))

    @commands.command(aliases = ['FBI' , 'Fbi'])
    async def fbi(self , ctx , * , text = ''):
        await start_log("fbi")
        await update_log("fbi")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to provide some text.')

        if len(text) > 32:
            return await ctx.send('Your text cannot exceed 32 characters.')

        img = Image.open('fbi.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf' , 60)

        draw.text((45,450) , text , (0,0,0) , font = font)

        img.save('fbiout.jpg')
        await ctx.send(file = discord.File('fbiout.jpg'))

    @commands.command(aliases = ['Slap' , 'SLAP'])
    async def slap(self , ctx , user : discord.Member = None):
        await start_log("slap")
        await update_log("slap")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if user is None:
            return await ctx.send('You need to mention someone to use this command.')

        if user == ctx.author:
            return await ctx.send('You cannot slap yourself. Please mention someone else.')

        bg = Image.open('slap.jpg')
        authorAsset = ctx.author.avatar_url_as(format = 'jpg' , size=128)
        userAsset = user.avatar_url_as(format = 'jpg' , size=128)

        authorData = BytesIO(await authorAsset.read())
        userData = BytesIO(await userAsset.read())
        authorPFP = Image.open(authorData) # 298
        userPFP = Image.open(userData) #338
        authorPFP = authorPFP.resize((298,298))
        userPFP = userPFP.resize((338,338))
        bg.paste(authorPFP , (479,94))
        bg.paste(userPFP , (815,334))

        bg.save('slapout.jpg')
        await ctx.send(file = discord.File('slapout.jpg'))

    @commands.command(aliases = ['Armor' , 'ARMOR' , 'Armour' , 'armour' , 'ARMOUR'])
    async def armor(self , ctx , * , text = ''):
        await start_log("armor")
        await update_log("armor")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        if len(text) > 60:
            return await ctx.send('your text cannot exceed 60 characters')

        img = Image.open('armor.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf' , size = 20)
        increment = 0
        if len(text) > 20:
            txt = ''
            while len(text) > 20:
                txt = text[0:19]
                draw.text((40,370+increment) , txt , (0,0,0) , font = font)
                text = text[19:]
                increment += 40

            draw.text((40,370+increment) , text , (0,0,0) , font = font)
        else:
            draw.text((40,370) , text , (0,0,0) , font = font)

        img.save('armorout.png')
        await ctx.send(file = discord.File('armorout.png'))


    @commands.command(aliases = ['Patrick' , 'PATRICK'])
    async def patrick(self , ctx , * , text = ''):
        await start_log("patrick")
        await update_log("patrick")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        #11 , 130 , 470
        img = Image.open('patrick.jpg')
        font = ImageFont.truetype('arial.ttf' , 40)
        draw = ImageDraw.Draw(img)
        
        if len(text) > 33:
            return await ctx.send('Your text cannot excceed 33 characters.')

        increment = 0
        if len(text) > 11:
            txt = ''
            while len(text) > 11:
                txt = text[0:10]
                draw.text((130,470+increment) , txt , (0,0,0) , font = font)
                increment += 70
                text = text[10:]

            draw.text((130,470+increment) , text , (0,0,0) , font = font)

        else:
            draw.text((130,470) , text , (0,0,0) , font = font)

        img.save('patrickout.jpg')
        await ctx.send(file = discord.File('patrickout.jpg'))

    @commands.command(aliases = ['Spongebob' , 'SPONGEBOB'])
    async def spongebob(self , ctx , * , text = ''):
        await start_log("spongebob")
        await update_log("spongebob")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        img = Image.open('spongebob.png')
        font = ImageFont.truetype('arial.ttf' , 30)
        draw = ImageDraw.Draw(img)
        
        if len(text) > 44:
            return await ctx.send('Your text cannot excceed 44 characters.')

        increment = 0
        if len(text) > 11:
            txt = ''
            while len(text) > 11:
                txt = text[0:10]
                draw.text((60,85+increment) , txt , (0,0,0) , font = font)
                increment += 40
                text = text[10:]

            draw.text((60,85+increment) , text , (0,0,0) , font = font)

        else:
            draw.text((60,85) , text , (0,0,0) , font = font)

        img.save('spongeout.png')
        await ctx.send(file = discord.File('spongeout.png'))

    @commands.command(aliases = ['Shit' , 'SHIT'])
    async def shit(self , ctx , * , text = ''):
        await start_log("shit")
        await update_log("shit")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        img = Image.open('shit.jpg')
        font = ImageFont.truetype('arial.ttf' , 15)
        draw = ImageDraw.Draw(img)
        
        if len(text) > 33:
            return await ctx.send('Your text cannot excceed 33 characters.')

        increment = 0
        if len(text) > 11:
            txt = ''
            while len(text) > 11:
                txt = text[0:10]
                draw.text((90,210+increment) , txt , (0,0,0) , font = font)
                increment += 30
                text = text[10:]

            draw.text((90,210+increment) , text , (0,0,0) , font = font)

        else:
            draw.text((90,210) , text , (0,0,0) , font = font)

        img.save('shitout.jpg')
        await ctx.send(file = discord.File('shitout.jpg'))

    @commands.command(aliases = ['Santa' , 'SANTA'])
    async def santa(self , ctx , * , text = ''):
        await start_log("santa")
        await update_log("santa")
        voted = await self.dblpy.get_user_vote(ctx.author.id)
        print(voted)
        if not voted:
            embed = discord.Embed(description = 'You Need to Upvote the bot to use this command.\nTo upvote the bot **[Click Here](https://top.gg/bot/757272442820362281/vote)**' , color = discord.Color.red())
            return await ctx.send(embed = embed)

        if text == '':
            return await ctx.send('You need to pass some text.')

        img = Image.open('santa.jpg')
        font = ImageFont.truetype('arial.ttf' , 30)
        draw = ImageDraw.Draw(img)
        
        if len(text) > 72:
            return await ctx.send('Your text cannot excceed 72 characters.')

        increment = 0
        if len(text) > 18:
            txt = ''
            while len(text) > 18:
                txt = text[0:17]
                draw.text((40,475+increment) , txt , (0,0,0) , font = font)
                increment += 40
                text = text[17:]

            draw.text((40,475+increment) , text , (0,0,0) , font = font)

        else:
            draw.text((40,475) , text , (0,0,0) , font = font)

        img.save('santaout.jpg')
        await ctx.send(file = discord.File('santaout.jpg'))

    @commands.command(aliases = ["Stats" , "STATS"])
    async def stats(self , ctx):
        users = await get_log_data()
        totalUsers  = get_count(self.client)
        c_count =  0
        for used in users:
            c_count += users[used]["count"]

        votes = await self.dblpy.get_bot_upvotes()

        embed = discord.Embed(title="Among us Bot stats!",description=f"==============\n**Servers** : `{len(self.client.guilds)}`\n**Commands** : `{c_count}`\n**Users** : `{totalUsers}`\n**Votes** : `{len(votes)}`\n==============", color=discord.Color.green())

        embed.set_thumbnail(url = "https://5droid.ru/uploads/posts/2020-02/1581588210_among-us.png")

        await ctx.send(embed = embed)

    @commands.command()
    async def help(self , ctx):
        await start_log("help")
        await update_log("help")
        h = Helpfunc(self.client)
        await h.start(ctx)


        
def setup(client):
    client.add_cog(Memes(client))