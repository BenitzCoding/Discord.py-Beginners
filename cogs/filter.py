import discord

from discord.utils import get
from discord.ext import commands

class Filter(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild.id == 780278916173791232:
			user = message.author
			guild = discord.utils.get(bot.guilds, id=780278916173791232)
			alart = discord.utils.get(guild.text_channels, id=789762003740262401)
			pings = ["@everyone", "@here"]
			blocked_invites = ["discord.gg", "discord.com/invite"]
			blocked_links = [".qp", ".cp", ".gp", ".pq", "http://", "https://", "www.", ".com", ".net", ".tk", ".uk", ".un", ".gov", ".us", ".cf", ".ml", ".bn", ".in", ".tech", ".bot", ".nu", ".gg", ".chat", ".xyz", ".ga", ".gp", ".org", ".eu", ".name", ".me", ".nl", ".tv", ".info", ".biz", ".cc", ".mobi", ".actor", ".academy", ".agency", ".accountant", ".ws", ".garden", ".cafe", ".ceo", ".care", ".art"]
			blocked_words = ["f**k", "fuk", "fuc", "fuck", "f*ck", "bitch", "b*tch", "n*gga", "ni**a", "nigga", "vegina", "fag", "f*g", "dick", "d*ck", "penis", "porn", "xnxx", "xxnx", "xxx", "sex", "s*x", "hentai", "henti", "pxrn", "p*rn", "a$$", "cunt", "c*nt", "boob", "tits", "cock", "f u c k", "s h i t", "b i t c h", "h e n t a i", "p o r n", "d!ck"]
			blacklisted_links = ["youtube.com", "mythicalkitten.com"]
			ip_grabbers = ["blasze.com", "iplogger.org", "2no.co", "iplogger.com", "iplogger.ru", "yip.su", "iplogger.co", "iplogger.info", "ipgrabber.ru", "iplis.ru", "02ip.ru", "ezstat.ru", "ps3cfw.com", "grabify.link", "lovebird.guru", "truelove.guru", "dateing.club", "otherhalf.life", "shrekis.life", "datasig.io", "datauth.io", "headshot.monster", "gaming-at-my.best", "progaming.monster", "yourmy.monster", "screenshare.host", "imageshare.best", "screenshot.best", "gamingfun.me", "catsnthing.com", "mypic.icu", "catsnthings.fun", "curiouscat.club", "joinmy.site", "fortnitechat.site", "fortnite.space", "freegiftcards.co", "stopify.co", "leancoding.co"]
			link_shorteners = ["ouo.io", "bit.ly", "shorte.st", "adf.ly", "bc.vc", "bit.do", "soo.gd", "7.ly", "5.gp", "tiny.cc", "zzb.bz", "adfoc.us", "my.su", "goo.gl"]

			tokens = [token for token in TOKEN_REGEX.findall(message.content) if validate_token(token)]
			if tokens and message.author.id != bot.user.id:
				await message.delete()
				embed = discord.Embed(title="Leaked Token", description="It looks like you've acidentally leaked your token, Make sure to regenerate your token at the [Developer Portal](https://discord.com/developers). Try your best to not leak your token again.", color=0x2F3136)
				embed.set_footer(text="Discord.py For Beginner", icon_url=logo)
				await user.send(embed=embed)

			for x in ip_grabbers:
				if x in message.content.lower():
					if message.author.guild_permissions.administrator:
						await bot.process_commands(message)
					else:
						await message.delete()
						blocked_ip_grabber = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a IP Grabber, The staff has been alarted and you will get your punishment accordingly.', color=0x2F3136)
						blocked_ip_grabber.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await user.send(embed=blocked_ip_grabber)

						report = discord.Embed(title='New Alart', color=0x2F3136)
						report.add_field(name='Reported User:', value=f'<@!{user.id}>({user.id}})', inline=False)
						report.add_field(name='IP Grabber Link:', value=f'```{message}```', inline=False)
						report.set_thumbnail(url=ctx.author.avatar_url)
						report.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await alart.send("@here")
						await alart.send(embed=report)

			for x in link_shorteners:
				if x in message.content.lower():
					if message.author.guild_permissions.administrator:
						await bot.process_commands(message)
					else:
						await message.delete()
						blocked_short = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a Link Shortner, please remove the shortner and send the actual link.', color=0x2F3136)
						blocked_short.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await user.send(embed=blocked_short)

						report = discord.Embed(title='New Alart', color=0x2F3136)
						report.add_field(name='Reported User:', value=f'<@!{user.id}>({user.id}})', inline=False)
						report.add_field(name='Shortened Link:', value=f'```{message}```', inline=False)
						report.set_thumbnail(url=ctx.author.avatar_url)
						report.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await alart.send(embed=report)
			
			for x in blocked_invites:
				if x in message.content.lower():
					if message.channel.id != 780280201162522634:
						await message.delete()
						blocked_invite = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained a Discord Invite, you may delete the blocked link and send the message again.', color=0x2F3136)
						blocked_invite.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await user.send(embed=blocked_invite)

			for x in pings:
				if x in message.content.lower():
					if message.author.guild_permissions.administrator:
						await bot.process_commands(message)
					else:
						await message.delete()
						await user.send("Please don't try to ping `@everyone` or `@here`. Your message has been removed.")

			for x in blocked_links:
				if x in message.content.lower():
					else:
						await message.delete()
						blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained blocked Links, you may delete the blocked link and send the message again.', color=0x2F3136)
						blocked_word.set_footer(text='Discord.py For Beginners', icon_url=logo)
						await user.send(embed=blocked_word)

			for x in blocked_words:
				if x in message.content.lower():
					await message.delete()
					blocked_word = discord.Embed(title='Blocked Message', description='Your message has been blocked because it contained Blocked Words, you may delete the blocked word and send the message again.', color=0x2F3136)
					blocked_word.set_footer(text='Discord.py For Beginners', icon_url=logo)
					await user.send(embed=blocked_word)

def setup(bot):
	bot.add_cog(Filter(bot))
