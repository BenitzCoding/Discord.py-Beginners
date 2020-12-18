import discord
from discord.ext import commands

# Emoji Definitions
removed_user = "https://images-ext-1.discordapp.net/external/FQNgUBUW_ueW0eMgsyOXZ_PWTp3bicrIa1BYVuVebMg/https/cdn.discordapp.com/emojis/469952898026045441.png"
unmute_infraction = "https://images-ext-1.discordapp.net/external/Sbcg9dEw8D8cZ76o0jnDL97MKdQ0jOSXbZPS4CzLDCc/https/cdn.discordapp.com/emojis/472472639206719508.png"
mute_infraction = "https://images-ext-1.discordapp.net/external/VxXsa6O2RyiK6GfSdeez3WSxPibPVu6X8B2d_c4PoVw/https/cdn.discordapp.com/emojis/472472640100106250.png"
forbidden = "<:F:780326063120318465>"
success = "<:D:780326344889860136>"
logo = 'https://cdn.discordapp.com/avatars/780320679886454784/8e052d72bce558b6ee31cecac3d80dca.png?size=1024'

# This prevents staff members from being punished 
class Sinner(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
		permission = argument.guild_permissions.manage_messages # can change into any permission
		if not permission: # checks if user has the permission
			return argument # returns user object
		else:
			raise commands.BadArgument(f"{forbidden} You can't use moderation commands against other staff members.") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
		muted = discord.utils.get(ctx.guild.roles, name="Muted") # gets role object
		if muted in argument.roles: # checks if user has muted role
			return argument # returns member object if there is muted role
		else:
			raise commands.BadArgument(f"{forbidden} The user was not muted.") # self-explainatory
			
# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx, user, reason):
	role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
	hell = discord.utils.get(ctx.guild.text_channels, name="you-are-muted") # retrieves channel named hell returns none if there isn't
	if not role: # checks if there is muted role
		try: # creates muted role 
			muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
			for channel in ctx.guild.channels: # removes permission to view and send in the channels 
				await channel.set_permissions(muted, send_messages=False,
											  read_message_history=False,
											  read_messages=False)
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} Bot does not have permission to create a `muted` role.") # self-explainatory
		await user.add_roles(muted) # adds newly created muted role
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Mute\n**Expires:** Permenant\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=mute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} muted user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} muted user *user was not notified*")
	else:
		await user.add_roles(role) # adds already existing muted role
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Mute\n**Expires:** Permenant\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=mute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} muted user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} muted user *user was not notified*")
	   
	if not hell: # checks if there is a channel named hell
		overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
					  ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
					  muted: discord.PermissionOverwrite(read_message_history=True)} # permissions for the channel
		try: # creates the channel and sends a message
			channel = await ctx.create_channel('you-are-muted', overwrites=overwrites)
			await channel.send("Checking if channel exists.")
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} Bot doesn't have create channel permission.")
			
			
class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def __error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send(error)
			
	@commands.command(aliases=["banish", "punish"])
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user: Sinner=None, reason=None):
		"""Casts users out of heaven."""
		
		if not user: # checks if there is a user
			return await ctx.send(f"{forbidden} No user was specified")
		
		if reason is None:
			return await ctx.send(f"{forbidden} Please provide a reason.")

		try:
			notify_user = discord.Embed(description=f"\n**Type:** Ban\n**Expires:** Permenant\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=removed_user)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} banned user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} banned user *user was not notified*")
		
		try: # Tries to ban user
			await ctx.guild.ban(user, reason=f"{reason}")
			await ctx.send(f"{user.mention} was cast out of heaven for {reason}.")
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} unable to ban user")

	@commands.command()
	async def softban(self, ctx, user: Sinner=None, reason=None):
		"""Temporarily restricts access to heaven."""
		
		if not user: # checks if there is a user
			return await ctx.send(f"{forbidden} No user was specified")
		
		if reason is None:
			return await ctx.send(f"{reason} Please provide a reason.")

		try:
			notify_user = discord.Embed(description=f"\n**Type:** Soft-Ban\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=removed_user)
			await user.send(embed=notify_user)
			await ctx.send(f"{success} soft-banned user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} soft-banned user *user was not notified*")

		try: # Tries to soft-ban user
			await ctx.guild.ban(user, reason=reason) 
			await ctx.guild.unban(user, "Soft-Ban Expired")
		except discord.Forbidden:
			return await ctx.send(f"{forbidden} unable to soft-ban user")
	
	@commands.command()
	async def mute(self, ctx, user: Sinner, reason=None):
		if reason is None:
			await ctx.send(f"{forbidden} Please provide a reason.")
		else:
			await mute(ctx, user, reason=reason) # uses the mute function
	
	@commands.command()
	async def kick(self, ctx, user: Sinner=None, reason=None):
		if not user: # checks if there is a user 
			return await ctx.send(f"{forbidden} No user was specified")
		
		if reason is None:
			return await ctx.send(f"{forbidden} Please provide a reason.")
		
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Kick\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=removed_user)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} kicked user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} kicked user *user was not notified*")

		else:
			try: # tries to kick user
				await ctx.guild.kick(user, reason=f"{reason}")
			except discord.Forbidden:
				return await ctx.send(f"{forbidden} unable to kick user")

	@commands.command()
	async def purge(self, ctx, limit: int):
		"""Bulk deletes messages"""
		
		await ctx.purge(limit=limit + 1) # also deletes your own message
		await ctx.send(f"{success} `{limit}` messages deleted.", delete_after=3) 
	
	@commands.command()
	async def unmute(self, ctx, user: Redeemed):
		"""Unmutes a muted user"""
		mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
		await user.remove_roles(mute_role, reason=f"User unmuted by {ctx.author.name}") # removes muted role
		try:
			notify_user = discord.Embed(description=f"You may now send messages in the server.", color=0x68C290)
			notify_user.set_author(name=f"You have been unmuted", icon_url=unmute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} unmuted user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} unmuted user *user was not notified*")

	@commands.command()
	async def block(self, ctx, user: Sinner=None):
		"""
		Blocks a user from chatting in current channel.
		   
		Similar to mute but instead of restricting access
		to all channels it restricts in current channel.
		"""
								
		if not user: # checks if there is user
			return await ctx.send(f"{forbidden} No user was specified")
								
		await ctx.set_permissions(user, send_messages=False) # sets permissions for current channel
		try:
			notify_user = discord.Embed(description=f"\n**Type:** Channel_Block\n**Expires:** Permenant\n**Reason:** `{reason}`", color=0xCD6D6D)
			notify_user.set_author(name=f"Infraction Information", icon_url=mute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} blocked user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} blocked user *user was not notified*")
	
	@commands.command()
	async def unblock(self, ctx, user: Sinner=None):
		"""Unblocks a user from current channel"""
								
		if not user: # checks if there is user
			return await ctx.send(f"{forbidden} You must specify a valid user")
		
		await ctx.set_permissions(user, send_messages=True) # gives back send messages permissions
		try:
			notify_user = discord.Embed(description=f"You may now send messages in <#{ctx.channel.id}>.", color=0x68C290)
			notify_user.set_author(name=f"You have been unblocked", icon_url=unmute_infraction)
			
			await user.send(embed=notify_user)
			await ctx.send(f"{success} unblocked user *user was notified*")
		except discord.Forbidden:
			await ctx.send(f"{success} unblocked user *user was not notified*")

	
								
								
def setup(bot):
	bot.add_cog(Moderation(bot))