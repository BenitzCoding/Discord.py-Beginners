import datetime
import platform
import discord
import aiohttp
import time

from psutil import virtual_memory
from discord.ext import commands
from psutil import cpu_percent
from discord import Spotify

from utils import functions
from utils.functions import func
from cogs.Core.Language import Language


config = functions.fetch("utils/cfg.json")
start_time = time.time()

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sinfo"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(colour = 0x27b1db)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "CreationDate"), value=ctx.guild.created_at.strftime("%d/%m/%Y at %H:%M:%S"), inline=False)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Owner"), value=ctx.guild.owner.name, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Region"), value=ctx.guild.region, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Roles"), value=len(ctx.guild.roles), inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Users"), value=ctx.guild.member_count, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Channels"), value=len(ctx.guild.channels), inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "AFKChannel"), value=ctx.guild.afk_channel, inline=True)
        embed.set_footer(icon_url=ctx.guild.icon_url, text=f"{ctx.guild.name} - {ctx.guild.id}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["rinfo"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def roleinfo(self, ctx, name=None):
        role = discord.utils.get(ctx.guild.roles, name=name)

        if not role:
            return await ctx.send(embed=func.BadResponseEmbed(self, ctx.guild.id, Language.get(ctx.guild.id, self.bot.cache, "Info", "Errors", "NoRole")))

        embed = discord.Embed(colour = 0x27b1db)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Rolename"), value=role.mention, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "RoleID"), value=role.id, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "UsersWRole"), value=len(role.members), inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Mentionable"), value=role.mentionable, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "DisplayedSep"), value=role.hoist, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Colour"), value=role.colour, inline=True)
        embed.set_footer(text="{} - {}".format(Language.get(ctx.guild.id, self.bot.cache, "Info", "RoleCreated"), role.created_at.strftime("%d/%m/%Y at %H:%M:%S")))
        await ctx.send(embed=embed)

    @commands.command(aliases=["uinfo"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
            pass
        if user.voice is None:
            channel = Language.get(ctx.guild.id, self.bot.cache, "Info", "NotInVc")
        else:
            channel = user.voice.channel.name
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    title = "{} {}, {}".format(Language.get(ctx.guild.id, self.bot.cache, "Info", "Listening"), activity.title, activity.artist)
                else:
                    title = "{} {}".format(Language.get(ctx.guild.id, self.bot.cache, "Info", "Playing"), activity.name)
        else:
            title = Language.get(ctx.guild.id, self.bot.cache, "Info", "Nothing")
        embed = discord.Embed(
            colour = 0x27b1db,
            timestamp = datetime.datetime.utcnow()
            )
        embed.set_footer(text="{}'s {}".format(user.name, Language.get(ctx.guild.id, self.bot.cache, "Info", "UserInfo")), icon_url=user.avatar_url)
        embed.set_author(name=title)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "JoinedAt"), value=user.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "AccCreated"), value=user.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Status"), value=user.status, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "RoleCount"), value=len(user.roles), inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Nick"), value=user.nick, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Voice"), value=channel, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def spotify(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
            pass
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(
                        description = "{} {}".format(Language.get(ctx.guild.id, self.bot.cache, "Info", "Listening"), activity.title),
                        colour = 0x27b1db,
                        )
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Artist"), value=activity.artist)
                    embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Album"), value=activity.album)

                    embed.set_footer(text="{} {}".format(Language.get(ctx.guild.id, self.bot.cache, "Info", "SongStart"), activity.created_at.strftime("%H:%M")))
                    await ctx.send(embed=embed)

    @commands.command(aliases=["binfo", "info"])
    @commands.guild_only()
    async def botinfo(self, ctx):
        activeServers = self.bot.guilds
        sum = 0
        for s in activeServers:
            sum += len(s.members)

        if self.bot.shard_ids != None:
            shardnum = self.bot.shard_ids.index(ctx.guild.shard_id) + 1
        else:
            shardnum = 1

        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))

        dapi = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/'):
                dapi2 = time.time()

        discordlatency = dapi2 - dapi

        wapi = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://116.203.154.166:8080/'):
                wapi2 = time.time()

        watchdoglatency = wapi2 - wapi


        connected_desc = f"""```
- Watchdog {config.version}
- Watchdog API ({int(round(watchdoglatency, 2) * 100)}ms)
- Discord API ({int(round(discordlatency, 2) * 100)}ms)
- {len(activeServers)} {Language.get(ctx.guild.id, self.bot.cache, "Info", "Guilds")}
- {sum} {Language.get(ctx.guild.id, self.bot.cache, "Info", "Users")}
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "Shards")} {shardnum} / {self.bot.shard_count} ({int(round(self.bot.latency, 2) * 100)}ms)
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "Cluster")} 0 / 0 (0ms)```"""

        coding_desc = f"""```
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "Language")}: Python {platform.python_version()}
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "Library")}: Discord.py
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "Version")}: {discord.__version__}```"""

        cluster_desc = f"""```
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "OS")}: {platform.system()}
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "CPU")}: {cpu_percent(interval=None, percpu=False)}%
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "RAM")}: {virtual_memory().percent}%
- {Language.get(ctx.guild.id, self.bot.cache, "Info", "Uptime")}: {uptime}```"""

        embed = discord.Embed(colour=0x27b1db)

        embed.set_author(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "BotInfo"))

        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Connected"), value=connected_desc, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Coding"), value=coding_desc, inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Info", "Cluster"), value=cluster_desc, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def credits(self, ctx):
        await ctx.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{}".format("\n".join(Language.get(ctx.guild.id, self.bot.cache, "Credits")))))

def setup(bot):
    bot.add_cog(InfoCommands(bot))
