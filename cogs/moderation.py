import discord
import json

from discord.ext import commands

# Emoji Definitions

removed_user = "https://images-ext-1.discordapp.net/external/FQNgUBUW_ueW0eMgsyOXZ_PWTp3bicrIa1BYVuVebMg/https/cdn.discordapp.com/emojis/469952898026045441.png"
unmute_infraction = "https://images-ext-1.discordapp.net/external/Sbcg9dEw8D8cZ76o0jnDL97MKdQ0jOSXbZPS4CzLDCc/https/cdn.discordapp.com/emojis/472472639206719508.png"
mute_infraction = "https://images-ext-1.discordapp.net/external/VxXsa6O2RyiK6GfSdeez3WSxPibPVu6X8B2d_c4PoVw/https/cdn.discordapp.com/emojis/472472640100106250.png"
forbidden = "<:F:780326063120318465>"
success = "<:D:780326344889860136>"
logo = 'https://cdn.discordapp.com/avatars/780320679886454784/8e052d72bce558b6ee31cecac3d80dca.png?size=1024'

#Classes

class Sinner(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument)
		permission = argument.guild_permissions.manage_messages
		if not permission:
			return argument 
		else:
			raise commands.BadArgument(f"{forbidden} You can't use moderation commands against other staff members.")


class Redeemed(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument)
		muted = discord.utils.get(ctx.guild.roles, name="Muted")
		if muted in argument.roles:
			return argument
		else:
			raise commands.BadArgument(f"{forbidden} {argument.name}#{argument.discriminator} was not muted.")
			
# Definitions

async def update_data(users, user):
	if not f'{user.id}' in users:
		users[f'{user.id}'] = {}
		users[f'{user.id}']['warns'] = 0

async def add_warns(users, user, warns):
	users[f'{user.id}']['warns'] += 1

async def mute(ctx, user, reason):
	role = discord.utils.get(ctx.guild.roles, name="Muted")
	hell = discord.utils.get(ctx.guild.text_channels, name="you-are-muted")
	if not role:
		try:
			muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
			for channel in ctx.guild.channels:
				await channel.set_permissions(muted, send_messages=False,
											  read_message_history=False,
											  read_messages=False)
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} Bot does not have permission to create a `muted` role.")
		await user.add_roles(muted)
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Mute\n**Expires:** N/A\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=mute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} muted {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} muted {user.name}#{user.discriminator} *User was not notified*")
	else:
		await user.add_roles(role) # adds already existing muted role
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Mute\n**Expires:** N/A\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=mute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} muted {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} muted {user.name}#{user.discriminator} *User was not notified*")
	   
	if not hell:
		overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
					  ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
					  muted: discord.PermissionOverwrite(read_message_history=True)}
		try:
			channel = await ctx.create_channel('you-are-muted', overwrites=overwrites)
			await channel.send("Checking if channel exists.")
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} Bot doesn't have create channel permission.")
			
# Main Cog

class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def __error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send(error)
			
	@commands.command(aliases=["banish", "punish"])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: Sinner=None, reason=None):
		
		if not user:
			return await ctx.send(f"{forbidden} No user was specified")
		
		if reason is None:
			return await ctx.send(f"{forbidden} Please provide a reason.")

		try:
			notify_user = discord.Embed(description=f"\n**Type:** Ban\n**Expires:** N/A\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=removed_user)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} banned {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} banned {user.name}#{user.discriminator} *User was not notified*")
		
		try:
			await ctx.guild.ban(user, reason=f"{reason}")
			await ctx.send(f"{user.mention} was cast out of heaven for {reason}.")
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} unable to ban user")

	@commands.command()
	async def softban(self, ctx, user: Sinner=None, reason=None):
		if not user:
			return await ctx.send(f"{forbidden} No user was specified")
		
		if reason is None:
			return await ctx.send(f"{reason} Please provide a reason.")

		try:
			notify_user = discord.Embed(description=f"\n**Type:** Soft-Ban\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=removed_user)
			await user.send(embed=notify_user)
			await ctx.send(f"{success} soft-banned {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} soft-banned {user.name}#{user.discriminator} *User was not notified*")

		try:
			await ctx.guild.ban(user, reason=reason) 
			await ctx.guild.unban(user, "Soft-Ban Expired")
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} unable to soft-ban user")
	
	@commands.command()
	async def mute(self, ctx, user: Sinner, *, reason=None):
		if reason is None:
			await ctx.send(f"{forbidden} Please provide a reason.")
		else:
			await mute(ctx, user, reason=reason)
	
	@commands.command()
	async def kick(self, ctx, user: Sinner=None, *, reason=None):
		if not user:
			return await ctx.send(f"{forbidden} No user was specified")
		
		if reason is None:
			return await ctx.send(f"{forbidden} Please provide a reason.")
		
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Kick\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=removed_user)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} kicked {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} kicked {user.name}#{user.discriminator} *User was not notified*")

		else:
			try:
				await ctx.guild.kick(user, reason=f"{reason}")
			except discord.Forbidden:
				return await ctx.send(f"{forbidden} unable to kick user")

	@commands.command()
	async def purge(self, ctx, limit: int):
		await ctx.purge(limit=limit + 1)
		await ctx.send(f"{success} `{limit}` messages deleted.", delete_after=3) 
	
	@commands.command()
	async def unmute(self, ctx, user: Redeemed):
		mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
		await user.remove_roles(mute_role, reason=f"User unmuted by {ctx.author.name}")
		try:
			notify_user = discord.Embed(description=f"You may now send messages in the server.", color=0x68C290)
			notify_user.set_author(name=f"You have been unmuted", icon_url=unmute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} unmuted {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} unmuted {user.name}#{user.discriminator} *User was not notified*")

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def block(self, ctx, user: Sinner=None, *, reason=None):

		if not user:
			return await ctx.send(f"{forbidden} No user was specified")

		if reason is None:
			return await ctx.send(f"{forbidden} Please Provide a reason.")

		await ctx.set_permissions(user, send_messages=False)
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Channel_Block\n**Expires:** N/A\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=mute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} blocked {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} blocked {user.name}#{user.discriminator} *User was not notified*")
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def unblock(self, ctx, user: Sinner=None):
								
		if not user:
			return await ctx.send(f"{forbidden} You must specify a valid user")
		
		await ctx.set_permissions(user, send_messages=True)
		try:
			notify_user = discord.Embed(description=f"You may now send messages in <#{ctx.channel.id}>.", color=0x68C290)
			notify_user.set_author(name=f"You have been unblocked", icon_url=unmute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} unblocked {user.name}#{user.discriminator} *User was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} unblocked {user.name}#{user.discriminator} *User was not notified*")
				
def setup(bot):
	bot.add_cog(Moderation(bot))