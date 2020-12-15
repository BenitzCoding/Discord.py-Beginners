import discord
import datetime

from discord.ext import commands, tasks

from utils import sql
from utils.functions import func
from cogs.Core.Language import Language


class MuteModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.muted = {}
        self.unmuteUsers.start()

    @tasks.loop(seconds=5)
    async def unmuteUsers(self):
        for guild in self.muted:
            for user in self.muted[guild]:
                if datetime.datetime.utcnow() > self.muted[guild][user]:
                    guild = self.bot.get_guild(guild)
                    role = discord.utils.get(guild.roles, name="muted")
                    member = guild.get_member(user)
                    try:
                        await member.remove_roles(role)
                    finally:
                        await member.send(embed=func.Alert(self, member, guild, Language.get(guild.id, self.bot.cache, "Moderator", "Unmuted"), "Watchdog", "Expired", None))
                        channel = await self.bot.fetch_channel(self.bot.cache[guild.id]["Logs"])
                        if channel:
                            await channel.send(embed=func.GoodResponseEmbed(self, guild.id, "{} {}".format(member.name, Language.get(guild.id, self.bot.cache, "Moderator", "NoLongerMuted"))))
                        sql.LogMe(guild.id, 4, "{} {} {}".format("Watchdog", Language.get(guild.id, self.bot.cache, "Moderator", "Unmuted"), member.name))
                        del self.muted[guild][user]

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join_(self, member):
        role = discord.utils.get(member.guild.roles, name="muted")
        if member.guild.id in self.muted:
            if member.id in self.muted[member.guild.id]:
                await member.add_roles(role)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member=None, duration=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        role = discord.utils.get(ctx.guild.roles, name="muted")
        channel = await self.bot.fetch_channel(self.bot.cache[ctx.guild.id]["Logs"])

        if not role:
            return

        if not member or member.bot:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "MuteNoUser")), delete_after=15)

        if not duration:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "Duration")), delete_after=15)

        if not any(char.isdigit() for char in duration):
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "InvalidDur")), delete_after=15)

        time = self.timeformat(duration)

        if time and time < 1 or time > 2678400:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "Duration")), delete_after=15)

        if role in member.roles:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "AlreadyMuted")), delete_after=15)

        endtime = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)

        if not ctx.guild.id in self.muted:
            self.muted[ctx.guild.id] = {}

        self.muted[ctx.guild.id][member.id] = endtime

        endtime = endtime.strftime("%d/%m/%Y at %H:%M:%S")

        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {}".format(member.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "MutedTo"), endtime)), delete_after=15)
        await member.send(embed=func.Alert(self, member, ctx.guild, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Muted"), ctx.author.name, None, endtime))
        if channel:
            await channel.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {} {}".format(member.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "MutedTo"), endtime)))
        await member.add_roles(role)
        sql.LogMe(ctx.guild.id, 4, "{} ({}) {} {}".format(ctx.author.display_name, ctx.author.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Muted"), member.name))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def unmute(self, ctx, member: discord.Member=None):

        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send(embed=func.NoPerm(self, ctx.guild.id), delete_after=15)

        role = discord.utils.get(ctx.guild.roles, name="muted")
        channel = await self.bot.fetch_channel(self.bot.cache[ctx.guild.id]["Logs"])

        if not role:
            return

        if not member:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "MuteNoUser")), delete_after=15)

        if not role in member.roles:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Errors", "NotMuted")), delete_after=15)

        del self.muted[ctx.guild.id][member.id]
        await member.remove_roles(role)
        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {}".format(member.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "NoLongerMuted"))), delete_after=15)
        await member.send(embed=func.Alert(self, member, ctx.guild, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Unmuted"), ctx.author.name))
        if channel:
            await channel.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {}".format(member.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "NoLongerMuted"))))
        sql.LogMe(ctx.guild.id, 4, "{} ({}) {} {}".format(ctx.author.display_name, ctx.author.name, Language.get(ctx.guild.id, self.bot.cache, "Moderator", "Unmuted"), member.name))

    def timeformat(self, st):

        available_times = ['s', 'm', 'h', 'd', 'w']
        multiplier = [1, 60, 3600, 86400, 604800]
        time = ''

        try:
            for i in st:
                try:
                    time += str(int(i))
                except:
                    if i in available_times:
                        time += i
                        break
        except:
            return False

        if time == '':
            return False

        for i, v in enumerate(available_times):
            if v in time:
                return int(time[:-1]) * multiplier[i]

        try:
            return int(time)
        except:
            pass

        return False

    def MutedEmbed(self, title, action, where, duration=None):
            embed = discord.Embed(colour=0xc70300)
            embed.set_author(name=title)
            embed.add_field(name=f"Action", value=action, inline=True)
            embed.add_field(name=f"Where", value=where, inline=True)
            if duration:
                embed.add_field(name=f"Expires", value=duration, inline=True)

            return embed



def setup(bot):
    bot.add_cog(MuteModule(bot))
