import discord
import json

from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Language import Language

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("./data/sniper.json") as f:
            self.sniper = json.load(f)

    # Adds overwrites to new channels
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        role = discord.utils.get(channel.guild.roles, name="muted")

        if not role:
            return

        if channel.guild.id in self.bot.cache:
            if self.bot.cache[channel.guild.id]["Logs"]:
                channel = await self.bot.fetch_channel(self.bot.cache[channel.guild.id]["Logs"])

        try:
            await channel.set_permissions(role, send_messages=False, add_reactions=False)
        except:
            if channel:
                await channel.send(embed=func.BadResponseEmbed(self, channel.guild.id, "{} {}".format(Language.get(channel.guild.id, self.bot.cache, "Errors", "CantSetOverwrite"), channel.name)))

    # Updates User Count
    @commands.Cog.listener()
    async def on_member_join(self, member):
        activeServers = self.bot.guilds
        sum = 0
        for s in activeServers:
            sum += len(s.members)
        people = format(sum, ",")
        watch = discord.Activity(type=discord.ActivityType.watching, name=f"{people} people | w!help")
        await self.bot.change_presence(activity=watch)

    # Updates User Count + Adds SQL Data
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        activeServers = self.bot.guilds
        sum = 0
        for s in activeServers:
            sum += len(s.members)
        people = format(sum, ",")
        watch = discord.Activity(type=discord.ActivityType.watching, name=f"{people} people | w!help")
        await self.bot.change_presence(activity=watch)

        sql.AddData(guild.id)

        sql.LogMe(guild.id, 1, "{} {}".format(Language.get(guild.id, self.bot.cache, "Events", "Added"), guild.name))

        muted_role = discord.utils.get(guild.roles, name="muted")

        if not muted_role:
            try:
                role = await guild.create_role(name="muted")
            except:
                try:
                    return await guild.owner.send(embed=func.BadResponseEmbed(self, guild.id, "{} {}setup @ {}".format(Language.get(guild.id, self.bot.cache, "Core", "Error", "CantCreateMutedRole"), "w!", guild.name)))
                except:
                    return

        Failed = []
        for channel in guild.channels:
            if channel.type != "voice":
                if not channel.overwrites_for(muted_role):
                    try:
                        await channel.set_permissions(role, send_messages=False, add_reactions=False)
                    except:
                        Failed.append(channel.name)
                        pass

        if len(Failed) > 0:
            try:
                return await guild.owner.send(embed=func.BadResponseEmbed(self, guild.id, "{}\n\n {}".format(Language.get(guild.id, self.bot.cache, "Errors", "CantSetOverwrite"), "\n".join(Failed))))
            except:
                return

    # Updates User Count + Removes SQL Data
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        activeServers = self.bot.guilds
        sum = 0
        for s in activeServers:
            sum += len(s.members)
        people = format(sum, ",")
        watch = discord.Activity(type=discord.ActivityType.watching, name=f"{people} people | w!help")
        await self.bot.change_presence(activity=watch)

        sql.RemoveData(guild.id)

        sql.LogMe(guild.id, 2, "{} {}".format(Language.get(guild.id, self.bot.cache, "Events", "Removed"), guild.name))

    # Snipe command
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        if not str(message.guild.id) in self.sniper:
            self.sniper[str(message.guild.id)] = {}
            with open("./data/sniper.json", "w") as f:
                json.dump(self.sniper, f, indent=4)

        if not str(message.channel.id) in self.sniper[str(message.guild.id)]:
            self.sniper[str(message.guild.id)][str(message.channel.id)] = {}
            with open("./data/sniper.json", "w") as f:
                json.dump(self.sniper, f, indent=4)

        self.sniper[str(message.guild.id)][str(message.channel.id)] = {"Message": message.content, "AuthorID": f"{message.author.id}"}
        with open("./data/sniper.json", "w") as f:
            json.dump(self.sniper, f, indent=4)


    # Functions

    def Embed(self, author, title, description):
        embed = discord.Embed(
                title = title,
                description = description,
                colour = 0xc70300
                )
        embed.set_author(name=author, icon_url=self.bot.user.avatar_url)

        return embed

def setup(bot):
    bot.add_cog(Events(bot))
