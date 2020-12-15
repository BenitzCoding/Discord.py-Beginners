import discord
import json

from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class WarnModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member=None, reason=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        if not member:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "WarnNoUser")), delete_after=15)

        if not reason:
            reason = Language.get(ctx.guild.id, self.bot.cache, "Moderator", "NoReason")

        channel = await self.bot.fetch_channel(self.bot.cache[ctx.guild.id]["Logs"])

        sql.Warn(ctx.guild.id, member.id, ctx.author.id, reason)

        await member.send(embed=func.Alert(self, member, ctx.guild, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Warned"), ctx.author, reason))
        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {} | {}: {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WasWarned"), ctx.author.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason)))
        await Rules.DoRule(self, member, ctx.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)
        if channel:
            await channel.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {} | {}: {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WasWarned"), ctx.author.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason)))
        sql.LogMe(ctx.guild.id, 5, "{} ({}) {} {}. {}: {}".format(ctx.author.display_name, ctx.author.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Warned"), member.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), reason))

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.guild_only()
    async def infractions(self, ctx, member: discord.Member=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        if not member:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NoInfractionsUser")), delete_after=15)

        infr = sql.GetInfractions(ctx.guild.id, member.id)

        if not infr:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, "{} {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "HasNoInfractions"))), delete_after=15)

        embed = discord.Embed(colour = 0x27b1db)

        for i in infr:
            u = await self.bot.fetch_user(i[3])
            desc = "{} {} {} @ {} | {}: {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "WarnedBy"), u.mention, i[5], Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Reason"), i[4])
            embed.add_field(name="{}: {}".format(Language.get(ctx.guild.id, self.bot.cache, "Moderator", "InfractID"), i[0]), value=desc, inline=False)

        await ctx.send(embed=embed)

    @infractions.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def remove(self, ctx, member: discord.Member=None, id=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        if not member:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NoInfractionsUser")), delete_after=15)

        if not id:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, "{} {}{}".format(Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NeedID"), ctx.prefix, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NeedIDEnd"))), delete_after=15)

        rm = sql.RemoveInfraction(id, ctx.guild.id, member.id)
        channel = await self.bot.fetch_channel(self.bot.cache[ctx.guild.id]["Logs"])

        if not rm:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, "{} {}: {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "DoesntHave"), id)), delete_after=15)

        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "InfractionRemoved"), id)))

        if channel:
            await channel.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {}".format(member.mention, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "InfractionRemoved"), id)))

        sql.LogMe(ctx.guild.id, 5, "{} ({}) {}: {} {} {}".format(ctx.author.display_name, ctx.author.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "UnWarned"), id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "From"), member.name))

def setup(bot):
    bot.add_cog(WarnModule(bot))
