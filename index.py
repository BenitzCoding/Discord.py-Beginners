import os
import io
import re
import json
import time
import base64
import asyncio
import discord
import inspect
import aiohttp
import datetime
import textwrap
import traceback
import contextlib

from random import choice
from datetime import date
from utils import functions
from discord.utils import get
from contextlib import redirect_stdout
from discord.ext import commands, tasks
from discord_webhook import DiscordWebhook, DiscordEmbed
from discord.ext.commands import has_permissions, MissingPermissions, errors

intents = discord.Intents.default()
intents.members = True

bot = commands.AutoShardedBot(command_prefix=["!", "<@!780320679886454784>", "<@!780320679886454784> "], intents=intents)

bot.remove_command('help')

TOKEN = ''
logo = 'https://cdn.discordapp.com/avatars/780320679886454784/8e052d72bce558b6ee31cecac3d80dca.png?size=1024'

config = functions.fetch("utils/cfg.json")
functions.boot()
bot.cache = {}

# Status

@tasks.loop(seconds=10)
async def status_task():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(bot.users)} Members'))
	await asyncio.sleep(10)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='DiscordPython.tk'))
	await asyncio.sleep(10)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Command: !help'))
	await asyncio.sleep(10)

# Bot Events Below:

# Bot Inizialization/ready event

@bot.event
async def on_ready():
	bot.session = aiohttp.ClientSession(loop=bot.loop)
	bot.owner_id = (await bot.application_info()).owner.id
	print('')
	count = 0
	for guild in bot.guilds:
		print("Connected to {}".format(guild))
		count +=1

	activeServers = bot.guilds
	sum = 0
	for s in activeServers:
		sum += len(s.members)
	people = format(sum, ",")

	print('')
	print('Coded by Benitz Original#1317')
	print('')
	status_task.start()

# Member Join Event

@bot.event
async def on_member_join(member):
	if member.bot:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780400771975086090/1aG9XbOqyGwRnEdvYie3lvUYAWYyiGkhU_y29TABVHy9_tG5wZd73Fe5TLG1ozG_MlFM')
		embed = DiscordEmbed(title='<:a:780407857093935124> Bot Added', description=f'**Bot Name:**\n{member.name} \n\n**Bot ID:**\n{member.id} \n\n**Bot Invite:**\nhttps://discord.com/oauth2/authorize?client_id={member.id}&scope=bot&permissions=0', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()
	else:
		responces = [f'{member.name} Has Joined!', f'Welcome {member.name}!', f'{member.name} joined **Discord.py For Beginner**!', f'{member.name} Joined', f'{member.name} Welcome!']
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780322258824200203/UGR3Yi6727QrvzAbBbr-UOy5T-tSeOvpTYcdEJR2lktSnrFK79LLbrw4d7MKjtBaA2e-')
		embed = DiscordEmbed(title=f'{choice(responces)}', description=f'Hey <@{member.id}> Welcome to **Discord.py For Beginners**! \n\n Make sure you read <#780281370508394516> and you know the rules and all. \n Happy Coding!', color=0x2F3136)
		embed.set_thumbnail(url=f'{member.avatar_url}')
		embed.set_footer(text=f'New Discord.py Developer', icon_url=f'{logo}')
		webhook.add_embed(embed)
		webhook.execute()

		fm = discord.Embed(description="This is a Discord.py server for Beginners. You may ask for support and help others, If are not a Beginner and you know a lot of Discord.py, you can get the helper rank.\n You can ask a staff member to recieve the @help-me role, anyone can ping this role if they need help regaurding Discord.py, or any help in general.\n\n Make sure you read and fully understand this channel <#780281370508394516>. You might not know why you were punished If you don't read or understand <#780281370508394516> \n\n If you get kicked or you leave the server here is a link to join back! \n :link: https://discord.gg/C8zFM3D2rn", color=0x2F3136)
		fm.set_author(name="Discord.py For Beginners", icon_url=f"{logo}")
		fm.set_footer(text='Discord.py Official Bot', icon_url=logo)
		await member.send(embed=fm)

# Member Remove Event

@bot.event
async def on_member_remove(member):
	if member.bot:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780400771975086090/1aG9XbOqyGwRnEdvYie3lvUYAWYyiGkhU_y29TABVHy9_tG5wZd73Fe5TLG1ozG_MlFM')
		embed = DiscordEmbed(title='<:r:780734645779693568> Bot Removed', description=f'**Bot Name:**\n{member.name} \n\n **Bot ID:**\n{member.id}', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()
	else:
		return

# Error Handler

@bot.event
async def on_command_error(ctx, err):
	if isinstance(err, errors.CommandOnCooldown):
		await ctx.send(f":stopwatch: Command is on Cooldown, please try again in {err.retry_after:.2f} seconds.")
	elif isinstance(err, errors.MissingPermissions):
		await ctx.send(f"<:F:780326063120318465> You can't use that command.")
	elif isinstance(err, errors.CommandNotFound):
		pass
	else:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780323537507713035/2sOcxGJQvsSc3_UBGcBIX9bX7OdtmCjUqngeAIJG7hluCG8ZQ4m-YZafB_AARJ_RqzS9')
		embed = DiscordEmbed(title='An Error has occurred', description=f'Error: \n ```py\n{err}```', color=0x2F3136)
		embed.set_timestamp()
		embed.set_thumbnail(url=f'{logo}')
		webhook.add_embed(embed)
		webhook.execute()
		print(err)

# ModMail and Filter

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	else:
		if message.guild == None:
			badstr = [" ", ">", "<", "+", "=", ";", ":", "[", "]", "*", "'", '"', ",", ".", "{", "}", "|", "(", ")", "$", "#", "@", "!", "^", "%", "&", "`", "~"]

			Gamer = message.author
			authname = message.author.name
			guild = get(bot.guilds, id=780278916173791232)

			authname1 = authname
			for word in badstr:
				authname1 = authname1.replace(word, '')
				authdisc = message.author.discriminator
			try:
				channel = get(guild.text_channels, name=f'{authname1.lower()}-{authdisc.lower()}')
				embed = discord.Embed(title=f'DM from {message.author.name}#{message.author.discriminator}', description=f'User ID: **{message.author.id}** \n\n **Message:** \n `{message.content}`', color=0x00ff00)
				embed.set_footer(text='Created by Benitz Original#1317', icon_url=logo)
				embed.set_thumbnail(url=message.author.avatar_url)
				await channel.send(embed=embed)
				emoji = '<a:Y:780327135381422140>'
				await message.add_reaction(emoji)
			except AttributeError:
				category = bot.get_channel(781002010744979516)
				guild = get(bot.guilds, id=780278916173791232)
				await guild.create_text_channel(name=f'{authname1.lower()}-{authdisc.lower()}', overwrites=None, reason='New ModMail', category=category)
				channel = get(guild.text_channels, name=f'{authname1.lower()}-{authdisc.lower()}')
				embed2 = discord.Embed(title=f'DM from {message.author.name}#{message.author.discriminator}', description=f'User ID: **{message.author.id}** \n\n **Message:** \n `{message.content}`', color=0x00ff00)
				embed2.set_footer(text='Created by Benitz Original#1317', icon_url=logo)
				embed2.set_thumbnail(url=message.author.avatar_url)
				await channel.send(embed=embed2)
				emoji2 = '<a:Y:780327135381422140>'
				await message.add_reaction(emoji2)

# Deletion Log

@bot.event
async def on_message_delete(message):
	if message.author.bot:
		return
	else:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780323537507713035/2sOcxGJQvsSc3_UBGcBIX9bX7OdtmCjUqngeAIJG7hluCG8ZQ4m-YZafB_AARJ_RqzS9')
		embed = DiscordEmbed(title='Message Deleted', description=f'**Message Author:** \n <@!{message.author.id}>({message.author.name}#{message.author.discriminator}) \n\n **Message Channel:**\n<#{message.channel.id}> \n\n **Message Content:** \n ```{message.content}```', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()

# Bot Commands Below:

# ModMail End

@bot.command()
async def modclose(ctx, user: discord.Member):
	if ctx.author.guild_permissions.ban_members:
		if ctx.channel.category_id == 781002010744979516:
			notification = discord.Embed(title='ModMail Ended', description='This Modmail conversation has been ended, the Staff has been disconnected from the conversation.', color=0x2F3136)
			notification.set_footer(text='Discord.py For Beginners', icon_url=f'{logo}')
			await user.send(embed=notification)
			await ctx.send('<:D:780326344889860136> ModMail Ended. Deleting Channel in 5 seconds')
			await asyncio.sleep(5)
			await ctx.channel.delete(reason='ModMail Support Ended.')
		else:
			await ctx.message.delete()
			await ctx.send('<:F:780326063120318465> This channel is not a ModMail channel.', delete_after=3)
	else:
		await ctx.message.delete()
		await ctx.send('<:F:780326063120318465> You are not a Administrator, and this is not a ModMail Channel.', delete_after=5)

# Source Command

@bot.command(aliases = ["sourcecode", "source-code"])
async def source(ctx):
	embed = discord.Embed(title='Discord.py Beginner Source-Code', description="Here is the source Code for Discord.py Beginner's Official Bot.\n https://github.com/BenitzCoding/Discord.py-Begginners", color=0x2F3136)
	embed.set_image(url='https://media.discordapp.net/attachments/715492844768591945/783944318133600266/source.png?width=961&height=541')
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Reminder

@bot.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
	print(time)
	print(reminder)
	user = ctx.message.author
	embed = discord.Embed(color=0x2F3136)
	embed.set_footer(text="Discord.py For Beginners", icon_url=f"{logo}")
	seconds = 0
	if reminder is None:
		embed.add_field(name='Warning', value=' Run the command again but specify what do you want me to remind you about.') # Error message
	if time.lower().endswith("d"):
		seconds += int(time[:-1]) * 60 * 60 * 24
		counter = f"{seconds // 60 // 60 // 24} days"
	if time.lower().endswith("h"):
		seconds += int(time[:-1]) * 60 * 60
		counter = f"{seconds // 60 // 60} hours"
	elif time.lower().endswith("m"):
		seconds += int(time[:-1]) * 60
		counter = f"{seconds // 60} minutes"
	elif time.lower().endswith("s"):
		seconds += int(time[:-1])
		counter = f"{seconds} seconds"
	if seconds == 0:
		embed.add_field(name='Warning',
						value='Please specify a proper duration, do `!help reminder` for more information.')
	elif seconds < 300:
		embed.add_field(name='Warning',
						value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
	elif seconds > 7776000:
		embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
	else:
		beforermd = discord.Embed(title='Reminder Set', description=f'You will be reminded in {counter}', color=0x2F3136)
		beforermd.set_footer(text='Discord.py For Beginners', icon_url=logo)
		afterrmd = discord.Embed(title='Reminder', description=f'**Your reminder:** \n {reminder} \n\n *reminder set {counter} ago*', color=0x2F3136)
		afterrmd.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await ctx.send(embed=beforermd)
		await asyncio.sleep(seconds)
		await ctx.send(embed=afterrmd)
		return
	await ctx.send(embed=embed)

# Tempban

@bot.command(case_insensitive = True, aliases = ["temp-ban", "temp_ban"])
@commands.bot_has_permissions(ban_members = True)
async def tempban(ctx, user: discord.Member, time, *, reason):
	print(time)
	print(reminder)
	user = ctx.message.author
	embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
	embed.set_footer(text="Discord.py For Beginners", icon_url=f"{logo}")
	seconds = 0
	if reason is None:
		await ctx.send('<:F:780326063120318465> User not banned, because no reason was specified.') # Error message
	if time.lower().endswith("y"):
		seconds += int(time[:-1]) * 60 * 60 * 24 * 365
		counter = f"{seconds // 60 // 60 // 24 // 365} years"
	if time.lower().endswith("d"):
		seconds += int(time[:-1]) * 60 * 60 * 24
		counter = f"{seconds // 60 // 60 // 24} days"
	if time.lower().endswith("h"):
		seconds += int(time[:-1]) * 60 * 60
		counter = f"{seconds // 60 // 60} hours"
	elif time.lower().endswith("m"):
		seconds += int(time[:-1]) * 60 * 60 * 24 * 30
		counter = f"{seconds // 60 // 60 // 24 // 30} months"
	elif time.lower().endswith("s"):
		seconds += int(time[:-1])
		counter = f"{seconds} seconds"
	if seconds == 0:
		await ctx.send('<:F:780326063120318465> User not banned, because no time was specified.') 
	else:
		audit = get(guild.channels, id=780323115360190484)

		beforermd = discord.Embed(title='Banned User', description=f'User has been banned for {counter} \n\n **reason:**\n{reason}', color=0x2F3136)
		beforermd.set_footer(text='Discord.py For Beginners', icon_url=logo)
		
		log = discord.Embed(title='User Temp-Banned', description=f'**User:**\n<@!{user.id}>({user.name}#{user.discriminator}) \n\n **Moderator:**\n<@!{ctx.author.id}>({ctx.author.name}#{ctx.author.discriminator}) \n\n **Reason:**\n{reason}', color=0x2F3136)
		log.set_footer(text='Discord.py For Beginners', icon_url=logo)

		afterrmd = discord.Embed(title='User Unbanned', description=f'**User:**\n{user} \n\n **Unbanned after:**\n{counter}', color=0x2F3136)
		afterrmd.set_footer(title='Discord.py For Beginners', icon_url=logo)

		banned = discord.Embed(title='Discord.py For Beginners', description=f'You have been banned on **Discord.py For Beginners** for **{counter}**', color=0x2F3136)
		banned.set_footer(text='Discord.py For Beginners', icon_url=logo)

		await audit.send(embed=log)
		await ctx.send(embed=beforermd)
		await user.send(embed=banned)
		await ctx.guild.unban(user, reason=reason)
		await asyncio.sleep(seconds)
		await ctx.guild.unban(user)
		await audit.send(embed=afterrmd)
		return
	await ctx.send(embed=embed)

# ModMail Reply

@bot.command()
@commands.has_permissions(manage_messages=True)
async def modrep(ctx, user: discord.Member, *, message: str):
	try:
		embed = discord.Embed(title='Modmail Support', description=f'{message}', color=0x2F3136)
		embed.set_footer(text=f'Discord.py For Beginners', icon_url=logo)
		await user.send(embed=embed)
		await ctx.send(f"Notified User!")
	except discord.Forbidden:
		await ctx.send("Unable to notify user.")

# Add Bot Command

@bot.command()
async def addbot(ctx, curl, *, reason):
	if reason is None:
		reply = discord.Embed(title='Bot was not Requested', description='Your Bot was not requested, please specify a reason for your bot to be added.', color=0x2F3136)
		reply.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await ctx.message.delete()
		await ctx.send(embed=reply, delete_after=5)

	else:
		webhook = DiscordWebhook(url='webhook url')
		embed = DiscordEmbed(title='New Bot Request', description=f'Bot Requested by <@!{ctx.author.id}> \n\n**Reason:**\n{reason}\n\n:link: [Bot Invite](https://discord.com/oauth2/authorize?client_id={curl}&scope=bot&permissions=0)', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()

		webhook2 = DiscordWebhook(url='webhook url')
		embed2 = DiscordEmbed(title='New Bot Request', description=f'Bot Requested by <@!{ctx.author.id}> \n\n**Reason to add bot:** \n{reason}', color=0x2F3136)
		embed2.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook2.add_embed(embed2)
		webhook2.execute()

		reply = discord.Embed(title='Bot has been Requested', description='Your Bot has been requested, if this was a troll, or a prank, you will be punished.', color=0x2F3136)
		reply.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await ctx.message.delete()
		await ctx.send(embed=reply, delete_after=5)

#Bot Approve Command

@bot.command()
@commands.has_permissions(administrator=True)
async def approve(ctx, user: discord.Member, *, reason: commands.clean_content):
	if reason is None:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780400771975086090/1aG9XbOqyGwRnEdvYie3lvUYAWYyiGkhU_y29TABVHy9_tG5wZd73Fe5TLG1ozG_MlFM')
		embed = DiscordEmbed(title='<:D:780326506366500864> Bot Request Approved', description=f'**Approved By:** {ctx.author.mention}({ctx.author.name}#{ctx.author.discriminator}) \n\n**Bot Owner:** {user.mention}({user.name}#{user.discriminator}) \n\n**Reason:**\n**NOT SPECIFIED**', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()
		await ctx.send('<:D:780326506366500864> Bot Approved')
	else:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780400771975086090/1aG9XbOqyGwRnEdvYie3lvUYAWYyiGkhU_y29TABVHy9_tG5wZd73Fe5TLG1ozG_MlFM')
		embed = DiscordEmbed(title='<:D:780326506366500864> Bot Request Approved', description=f'**Approved By:** {ctx.author.mention}({ctx.author.name}#{ctx.author.discriminator}) \n\n**Bot Owner:** {user.mention}({user.name}#{user.discriminator}) \n\n**Reason:**\n{reason}', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()
		await ctx.send('<:D:780326506366500864> bot Approved')

# Bot Disapprove Command

@bot.command()
@commands.has_permissions(administrator=True)
async def disapprove(ctx, user: discord.Member, *, reason: commands.clean_content):
	if reason is None:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780400771975086090/1aG9XbOqyGwRnEdvYie3lvUYAWYyiGkhU_y29TABVHy9_tG5wZd73Fe5TLG1ozG_MlFM')
		embed = DiscordEmbed(title='<:F:780326063120318465> Bot Request Disapproved', description=f'**Disapproved By:** {ctx.author.mention}({ctx.author.name}#{ctx.author.discriminator}) \n\n**Bot Owner:** {user.mention}({user.name}#{user.discriminator}) \n\n**Reason:**\n**NOT SPECIFIED**', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()
		await ctx.send('<:F:780326063120318465> Bot Disapproved!')
	else:
		webhook = DiscordWebhook(url='https://discord.com/api/webhooks/780400771975086090/1aG9XbOqyGwRnEdvYie3lvUYAWYyiGkhU_y29TABVHy9_tG5wZd73Fe5TLG1ozG_MlFM')
		embed = DiscordEmbed(title='<:F:780326063120318465> Bot Request Disapproved', description=f'**Disapproved By:** {ctx.author.mention}({ctx.author.name}#{ctx.author.discriminator}) \n\n**Bot Owner:** {user.mention}({user.name}#{user.discriminator}) \n\n**Reason:**\n{reason}', color=0x2F3136)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		webhook.add_embed(embed)
		webhook.execute()
		await ctx.send('<:F:780326063120318465> Bot Disapproved')

# Help Group

@bot.group()
async def help(ctx):
	if ctx.invoked_subcommand is None:
		embed = discord.Embed(timestamp=ctx.message.created_at, title='Discord Python Official Bot', description='You can do `!help <command>` to get more info about the command.', color=0x2F3136)
		embed.add_field(name='<:D:780326506366500864> Staff Commands', value='```approve, disapprove, modrep, modclose, check, shutdown```')
		embed.add_field(name='<:C:780327572847853628> User Commands', value='```addbot, eval, ping, avatar, about, report, ticket, close```')
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await ctx.send(embed=embed)

# ModRep Help

@help.command(name='modrep')
async def help_modrep(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='ModRep Command')
	embed.add_field(name='Command Description:', value='This command is used to reply to the user on a modmail.', inline=False)
	embed.add_field(name='Command Permissions:', value='`MANAGE_MESSAGES`', inline=False)
	embed.add_field(name='Usage:', value='```py\n!modrep <@!userID> <messsage>```', inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Ping Help

@help.command(name='ping')
async def help_ping(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Ping Command')
	embed.add_field(name='Command Description:', value="This command checks the bot's Webshock and Rest Ping.", inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value='```py\n!ping```', inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Report Help 

@help.command(name='report')
async def help_report(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Report Command')
	embed.add_field(name='Command Description:', value='This command sends and alert to Discord.py Staff members with your report reason.', inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value='```py\n!report <@!userID> <reason>```', inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Eval Help

@help.command(name='eval')
async def help_eval(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Eval Command')
	embed.add_field(name='Command Description:', value='This command gets the given code and executes and gives the results of the given code, this is a way of testing your code.', inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value="```py\n-eval \nprint('test')```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# About Help

@help.command(name='about')
async def help_about(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='About Command')
	embed.add_field(name='Command Description:', value='This command gives you general information about the Server.', inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!about```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Check Help

@help.command(name='check')
async def help_check(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Check Command')
	embed.add_field(name='Command Description:', value='This command gets the user info of a mentioned user.', inline=False)
	embed.add_field(name='Command Permissions:', value='`MANAGE_MESSAGES`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!check <@!userID>```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Avatar Help

@help.command(name='avatar')
async def help_avatar(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Avatar Command')
	embed.add_field(name='Command Description:', value='This command shows the avatar of a mentioned user.', inline=False)
	embed.add_field(name='Command Permissions:', value='``', inline=False)
	embed.add_field(name='Usage:', value="```py\n!avatar <@!userID>``` or ```py\n!avatar```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Shutdown Help

@help.command(name='shutdown')
async def help_shutdown(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Shutdown Command')
	embed.add_field(name='Command Description:', value='This command Shuts Down the bot.', inline=False)
	embed.add_field(name='Command Permissions:', value='`OWNER_ONLY`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!shutdown```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Add Bot Help

@help.command(name='addbot')
async def help_addbot(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Add Bot Command')
	embed.add_field(name='Command Description:', value='This command sends a the bot request to the staff with a generated invite, for the staff members to review the bot.', inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!addbot <BotID> <reason>```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Approve Help

@help.command(name='approve')
async def help_approve(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Approve Command')
	embed.add_field(name='Command Description:', value="This command Approves a user's requested bot and notifies the user that the bot has been approved.", inline=False)
	embed.add_field(name='Command Permissions:', value='`ADMINISTRATOR`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!approve <@userID> <reason>```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Disapprove Help

@help.command(name='disapprove')
async def help_disapprove(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Disapprove Command')
	embed.add_field(name='Command Description:', value="This command Disapproves a user's requested bot and notifies the user that the bot has been disapproved.", inline=False)
	embed.add_field(name='Command Permissions:', value='`ADMINISTRATOR`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!disapprove <@userID> <reason>```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Ticket Help

@help.command(name='ticket')
async def help_ticket(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Ticket Command')
	embed.add_field(name='Command Description:', value="This command will create a ticket with a provided reason.", inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!ticket <reason>```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Ticket Close Help

@help.command(name='close')
async def help_close(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Close Command')
	embed.add_field(name='Command Description:', value="This command will Delete your ticket after you're done.", inline=False)
	embed.add_field(name='Command Permissions:', value='`@everyone`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!close```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# ModMail Close Help

@help.command(name='modclose')
async def help_modclose(ctx):
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.set_author(name='Mod Close Command')
	embed.add_field(name='Command Description:', value="This command will End the ModMail support.", inline=False)
	embed.add_field(name='Command Permissions:', value='`BAN_MEMBERS`', inline=False)
	embed.add_field(name='Usage:', value="```py\n!modclose <@userID>```", inline=False)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Report Command

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def report(ctx, suspect: discord.Member, *, crime: commands.clean_content):
	if crime == None:
		embed = discord.Embed(title='<:F:780326063120318465> No Report Sent', description="No reports have been sent because you didn't specify any reason for your Report.")
	else:
		guild = get(bot.guilds, id=780278916173791232)
		channel = get(guild.text_channels, id=781370368702808064)
		
		report = discord.Embed(title='New Report', color=0x2F3136)
		report.add_field(name='Reporter:', value=f'<@!{ctx.author.id}>({ctx.author.name}#{ctx.author.discriminator})', inline=False)
		report.add_field(name="Reporter's ID:", value=f'{ctx.author.id}', inline=False)
		report.add_field(name='Reported User:', value=f'<@!{suspect.id}>({suspect.name}#{suspect.discriminator})', inline=False)
		report.add_field(name="Reported User's ID:", value=suspect.id, inline=False)
		report.add_field(name='Reason:', value=f'{crime}', inline=False)
		report.set_thumbnail(url=ctx.author.avatar_url)
		report.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await channel.send(embed=report)

		response = discord.Embed(title='<:D:780326506366500864> Report Sent', description='Your Report has been sent to **Discord.py For Beginner** Staff \n Our staff will review your report and take actions accordingly.', color=0x2F3136)
		response.set_footer(text='Discord.py For Beginner', icon_url=logo)
		await ctx.send(embed=response, delete_after=5)

# Ticket Close

@bot.command()
async def close(ctx):
	if ctx.channel.category_id == 780420074719936534:
		if ctx.channel.name == f'ticket-{ctx.author.discriminator}':
			await ctx.send('<:D:780326344889860136> Closing Ticket in 5 seconds.')
			await asyncio.sleep(5)
			await ctx.channel.delete(reason="Author of this ticket decided to close it.")
		elif ctx.author.guild_permissions.administrator:
			await ctx.send('<:D:780326344889860136> Closing Ticket in 5 seconds.')
			await asyncio.sleep(5)
			await ctx.channel.delete(reason="Author of this ticket decided to close it.")
		else:
			await ctx.send("<:F:780326063120318465> You can't close this ticket")
	else:
		await ctx.send(f"<:F:780326063120318465> This Channel is not a Ticket.")


# Ticket Command

@bot.command()
async def ticket(ctx, *, reason=None):
	if ctx.channel.id == 780418954236788737:
		if reason == None:
			await ctx.send("<:F:780326063120318465> Your Ticket was not created becaue you didn't specify a reason.")
		else:
			guild = get(bot.guilds, id=780278916173791232)
			overwrites = {
			guild.default_role: discord.PermissionOverwrite(read_messages=False),
			guild.me: discord.PermissionOverwrite(read_messages=True)
			}
			category = bot.get_channel(780420074719936534)
			chnl = await guild.create_text_channel(name=f'ticket-{ctx.author.discriminator}', overwrites=overwrites, reason='New Ticket', category=category)
			await chnl.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
			chan = discord.utils.get(guild.text_channels, name=f'ticket-{ctx.author.discriminator}')
			embed = discord.Embed(title=f"{ctx.author.name}'s Ticket", description=f"This Ticket has been created in **Discord.py For Beginners** Server\n\n**Reason:**\n{reason}", color=0x2F3136)
			embed.set_thumbnail(url=ctx.author.avatar_url)
			embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
			await chan.send(embed=embed)
			await ctx.send(f'<:D:780326344889860136> Your Ticket has been created! <#{chan.id}>')
	else:
		await ctx.send('<:F:780326063120318465> You can only create tickets in <#780418954236788737>.')

# About Command

@bot.command()
@commands.guild_only()
async def about(ctx):
	asd = get(ctx.guilds, id=780278916173791232)
	if ctx.guild.id == asd:
		embed = discord.Embed(timestamp=ctx.message.created_at, title='About')

		embed.add_field(name='Developer:', value='`Benitz Original#1317`')
		embed.add_field(name='Server Members:', value=f'{len(bot.users)}')
		embed.add_field(name='Server ID:', value='`780278916173791232`')
		embed.add_field(name='Server Owner:', value='`Benitz Original#1317`')
		embed.add_field(name='Server Creation Date:', value=asd.creation_at.__format__('%A, %d. %B %Y'))
		embed.add_field(name='Server Region:', value='`US Central`')
		embed.set_thumbnail(url=logo)
		embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
		await ctx.send(embed=embed)

	else:
		return

# Check Command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def check(ctx, user: discord.Member = None):
	if user is None:
		user = ctx.message.author
	if user.activity is not None:
		game = user.activity.name
	else:
		game = None
	voice_state = None if not user.voice else user.voice.channel
	embed = discord.Embed(timestamp=ctx.message.created_at, color=0x2F3136)
	embed.add_field(name='User ID:', value=user.id, inline=False)
	embed.add_field(name='Nick:', value=user.nick, inline=False)
	embed.add_field(name='Status:', value=user.status, inline=False)
	embed.add_field(name='On Mobile:', value=user.is_on_mobile(), inline=False)
	embed.add_field(name='In Voice:', value=voice_state, inline=True)
	embed.add_field(name='Game / Custom Status:', value=game, inline=False)
	embed.add_field(name='Highest Role:', value=user.top_role.name, inline=False)
	embed.add_field(name='Account Created Date:', value=user.created_at.__format__('%A, %d. %B %Y'))
	embed.add_field(name='Account Creation Time:', value=user.created_at.__format__('%H:%M:%S'))
	embed.add_field(name='Join Date:', value=user.joined_at.__format__('%A, %d. %B %Y'), inline=False)
	embed.add_field(name='Joined Time:', value=user.joined_at.__format__('%H:%M:%S'), inline=True)
	embed.set_thumbnail(url=user.avatar_url)
	embed.set_author(name=user.name, icon_url=user.avatar_url)
	embed.set_footer(text='Discord.py For Beginners', icon_url=logo)
	await ctx.send(embed=embed)

# Ping Command

@bot.command()
async def ping(ctx):
	before = time.monotonic()
	before_ws = int(round(bot.latency * 1000, 1))
	message = await ctx.send("🏓 Pong", delete_after=0)
	ping = (time.monotonic() - before) * 1000
	p = discord.Embed(title=f"Discord Python's Ping", description=f'WebShock Ping: `{before_ws}m/s` | Rest Ping: `{int(ping)}m/s`', color=0x2F3136)
	p.set_footer(text=f'Discord.py For Beginners', icon_url=f'{logo}')
	p.timestamp = datetime.utcnow()
	await ctx.send(embed=p)

# Shutdown Command

@bot.command()
async def shutdown(ctx):
	access = [529499034495483926, 635838945862746113]
	if ctx.author.id == access:
		await ctx.send('<:D:780326344889860136> Bot is shutting down.')
		await ctx.message.delete(ctx.message)
		await bot.change_presence(status=discord.Status.offline)
		await bot.logout()
	else:
		await ctx.send("<:F:780326063120318465> You don't have access to that command.")

# Read Cogs

for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		name = file[:-3]
		bot.load_extension(f"cogs.{name}")

# Run Bot

try:
	with open('./config.json') as f:
		token = json.load(f).get('token') or os.environ.get('token')
	bot.run(token, reconnect=True)
except Exception as e:
	print(e)
