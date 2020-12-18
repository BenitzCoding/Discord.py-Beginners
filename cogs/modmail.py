import discord

from discord.utils import get
from discord.ext import commands

logo = 'https://cdn.discordapp.com/avatars/780320679886454784/8e052d72bce558b6ee31cecac3d80dca.png?size=1024'

class ModMail(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return
		else:
			if message.guild == None:
				badstr = [" ", ">", "<", "+", "=", ";", ":", "[", "]", "*", "'", '"', ",", ".", "{", "}", "|", "(", ")", "$", "#", "@", "!", "^", "%", "&", "`", "~"]	

				Gamer = message.author
				authname = message.author.name
				guild = get(self.bot.guilds, id=780278916173791232)	

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
					category = self.bot.get_channel(781002010744979516)
					guild = get(self.bot.guilds, id=780278916173791232)
					await guild.create_text_channel(name=f'{authname1.lower()}-{authdisc.lower()}', overwrites=None, reason='New ModMail', category=category)
					channel = get(guild.text_channels, name=f'{authname1.lower()}-{authdisc.lower()}')
					embed2 = discord.Embed(title=f'DM from {message.author.name}#{message.author.discriminator}', description=f'User ID: **{message.author.id}** \n\n **Message:** \n `{message.content}`', color=0x00ff00)
					embed2.set_footer(text='Created by Benitz Original#1317', icon_url=logo)
					embed2.set_thumbnail(url=message.author.avatar_url)
					await channel.send(embed=embed2)
					emoji2 = '<a:Y:780327135381422140>'
					await message.add_reaction(emoji2)

def setup(bot):
	bot.add_cog(ModMail(bot))