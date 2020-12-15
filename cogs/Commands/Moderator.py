import discord
import json

from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Language import Language

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def ban(self, ctx, user : discord.User=None, *args):

        if not ctx.author.guild_permissions.ban_members:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        if not user:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "BanNoUser")), delete_after=15)

        reason = ' '.join(args)
        channel = await self.bot.fetch_channel(self.bot.cache[ctx.guild.id]["Logs"])

        if reason == "":
            reason = Language.get(ctx.guild.id, self.bot.cache, "Moderator", "NoReason")

        await user.send(embed=func.Alert(self, user, ctx.guild, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Banned"), ctx.author.name, reason))
        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {} | {}: {}".format(user.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WasBanned"), ctx.author.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason)))
        if channel:
            await channel.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {} | {}: {}".format(user.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WasBanned"), ctx.author.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason)))
        await ctx.guild.ban(user, reason=reason, delete_message_days=7)
        sql.LogMe(ctx.guild.id, 8, "{} ({}) {} {}. {}: {}".format(ctx.author.display_name, ctx.author.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Banned"), user.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def kick(self, ctx, user : discord.User=None, *args):

        if not ctx.author.guild_permissions.kick_members:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        if not user:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "KickNoUser")), delete_after=15)

        reason = ' '.join(args)
        channel = await self.bot.fetch_channel(self.bot.cache[ctx.guild.id]["Logs"])
        if reason == "":
            reason = Language.get(ctx.guild.id, self.bot.cache, "Moderator", "NoReason")

        await user.send(embed=func.Alert(self, user, ctx.guild, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Kicked"), ctx.author.name, reason))
        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {} | {}: {}".format(user.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WasKicked"), ctx.author.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason)))
        if channel:
            await channel.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {} | {}: {}".format(user.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WasKicked"), ctx.author.mention, Language.get( ctx.guild.id, self.bot.cache, "Moderator", "Reason"),reason)))
        await ctx.guild.kick(user, reason=reason)
        sql.LogMe(ctx.guild.id, 7, "{} ({}) {} {}. {}: {}".format(ctx.author.display_name, ctx.author.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Kicked"), user.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason))

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.guild_only()
    async def clear(self, ctx, amount : int=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        await ctx.message.delete()

        if not amount or amount > 100 or amount < 1:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "Upto100")), delete_after=15)

        dela = await ctx.channel.purge(limit=amount)
        await ctx.send("{}: {}".format(Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Deleted"), len(dela)), delete_after=15)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def snipe(self, ctx):

        with open("./data/sniper.json") as f:
            self.sniper = json.load(f)

            if not ctx.author.guild_permissions.manage_messages:
                return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)
            if not str(ctx.guild.id) in self.sniper:
                return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NoSnipeMessage")))
            if not str(ctx.channel.id) in self.sniper[str(ctx.guild.id)]:
                return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NoSnipeMessage")))

            user = await self.bot.fetch_user(self.sniper[str(ctx.guild.id)][str(ctx.channel.id)]["AuthorID"])

            embed = discord.Embed(colour=discord.Colour(0x27b1db), description=self.sniper[str(ctx.guild.id)][str(ctx.channel.id)]["Message"])

            embed.set_author(name=user.name, icon_url=user.avatar_url)

            await ctx.send(embed=embed)

            del self.sniper[str(ctx.guild.id)]
            with open("./data/sniper.json", "w") as f:
                json.dump(self.sniper, f, indent=4)

def setup(bot):
    bot.add_cog(ModCommands(bot))
