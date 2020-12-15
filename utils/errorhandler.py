import traceback
import datetime
import discord

from discord.ext import commands
from utils.functions import func
from cogs.Core.Language import Language

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.NoPrivateMessage, commands.DisabledCommand, discord.NotFound, commands.CheckFailure)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(embed=func.ErrorEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Errors", "BadArgument")), delete_after=15)

        elif isinstance(error, discord.Forbidden):
            try:
                return await ctx.send(embed=func.ErrorEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Errors", "Forbidden")), delete_after=15)
            except discord.Forbidden:
                return

        elif isinstance(error, commands.MissingPermissions):
            try:
                return await ctx.send(embed=func.ErrorEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Errors", "MissingPermissions")), delete_after=15)
            except discord.Forbidden:
                return

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=func.ErrorEmbed(self, ctx.guild.id, "{}! {}".format(ctx.author.mention, Language.get(ctx.guild.id, self.bot.cache, "Errors", "Cooldown"))), delete_after=15)

        await self.Errorlog(ctx, error)

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        await self.Errorlog(traceback.format_exc())

    async def Errorlog(self, ctx, error):
        errorschan = await self.bot.fetch_channel(705956719531917314)
        await errorschan.send(embed=func.ErrorEmbed(self, ctx, str(error)))

    def ErrorEmbed(self, ctx, error):
        embed = discord.Embed(
            title = "An error occurred.",
            description = error,
            colour = 0xebc634,
            timestamp=datetime.datetime.utcnow()
            )

        embed.add_field(name="Guild", value=ctx.guild.name, inline=True)
        embed.add_field(name="Command", value=ctx.command, inline=True)

        return embed


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
