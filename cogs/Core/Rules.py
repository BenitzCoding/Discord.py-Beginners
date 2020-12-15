import discord
import datetime

from discord.ext import commands, tasks

from utils import sql
from utils.functions import func
from cogs.Core.Language import Language

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muteLoop.start()
        self.kickLoop.start()
        self.banLoop.start()
        self.unmuteUsers.start()

        self.bot.tobemuted = {}
        self.bot.tobekicked = {}
        self.bot.tobebanned = {}

        self.muted = {}

    async def DoRule(self, user, guild, tobemuted, tobekicked, tobebanned):
        Rules = self.bot.cache[guild.id]["Rules"]
        Time = datetime.datetime.utcnow()
        CheckBefore = None

        if not Rules:
            return

        if not guild.id in tobemuted:
            tobemuted[guild.id] = []
        if not guild.id in tobekicked:
            tobekicked[guild.id] = []
        if not guild.id in tobebanned:
            tobebanned[guild.id] = []

        for rule in Rules:
            if rule[3] == 1: # If Minutes
                CheckBefore = Time - datetime.timedelta(minutes=rule[2])

            if rule[3] == 2: # If Hours
                CheckBefore = Time - datetime.timedelta(hours=rule[2])

            if rule[3] == 3: # If Days
                CheckBefore = Time - datetime.timedelta(days=rule[2])

            Infractions = sql.GetInfractionsAfter(user.id, guild.id, CheckBefore)

            if Infractions == rule[1]:
                if rule[0] == 1:
                    tobemuted[guild.id].append(user.id)
                if rule[0] == 2:
                    tobekicked[guild.id].append(user.id)
                if rule[0] == 3:
                    tobebanned[guild.id].append(user.id)

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
                        await member.send(embed=func.Alert(self, member, guild,Language.get(guild.id, self.bot.cache, "Moderator", "Unmuted"), "Watchdog", "Expired", None))
                        channel = await self.bot.fetch_channel(self.bot.cache[guild.id]["Logs"])
                        if channel:
                            await channel.send(embed=func.GoodResponseEmbed(self, guild.id, "{} {}".format(member.name, Language.get(guild.id, self.bot.cache, "Moderator","NoLongerMuted"))))
                        sql.LogMe(guild.id, 4, "{} {} {}".format("Watchdog", Language.get(guild.id, self.bot.cache, "Moderator", "Unmuted"), member.name))
                        del self.muted[guild][user]

    @tasks.loop(seconds=2)
    async def muteLoop(self):
        for guildid in self.bot.tobemuted:
            for userid in self.bot.tobemuted[guildid]:
                guild = self.bot.get_guild(guildid)
                member = guild.get_member(userid)
                role = discord.utils.get(guild.roles, name="muted")
                channel = await self.bot.fetch_channel(self.bot.cache[guild.id]["Logs"])
                if role:
                    if not role in member.roles:
                        try:
                            await member.add_roles(role)
                            endtime = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
                            if not guild.id in self.muted:
                                self.muted[guild.id] = {}
                            self.muted[guild.id][member.id] = endtime
                            endtime = endtime.strftime("%d/%m/%Y at %H:%M:%S")
                            await member.send(embed=func.Alert(self, member, guild, Language.get(guild.id, self.bot.cache, "Moderator", "Muted"), None, Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions"), endtime))
                            if channel:
                                await channel.send(embed=func.GoodResponseEmbed(self, guild.id, "{} {} {}".format(member.name, Language.get(guild.id, self.bot.cache, "Moderator", "MutedTo"), endtime)))
                            sql.LogMe(guild.id, 4, "{} {} {} {}: {}".format(Language.get(guild.id, self.bot.cache, "AutoMod", "Muted"), Language.get(guild.id, self.bot.cache, "Moderator", "Muted"), member.name, Language.get(guild.id, self.bot.cache, "Moderator", "Reason"), Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions")))
                        finally:
                            self.bot.tobemuted[guildid].remove(userid)
                else:
                    await member.send(embed=func.Alert(self, member, guild, Language.get(guild.id, self.bot.cache, "Moderator", "Muted"), None, Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions"), endtime))
                    if channel:
                        await channel.send(embed=func.GoodResponseEmbed(self, guild.id, "{} {} {}".format(member.name, Language.get(guild.id, self.bot.cache, "Moderator", "MutedTo"), endtime)))

                    sql.LogMe(guild.id, 4, "{} {} {} {}: {}".format(Language.get(guild.id, self.bot.cache, "AutoMod", "Muted"), Language.get(guild.id, self.bot.cache, "Moderator", "Muted"), member.name, Language.get(guild.id, self.bot.cache, "Moderator", "Reason"), Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions")))

    @tasks.loop(seconds=2)
    async def kickLoop(self):
        for guildid in self.bot.tobekicked:
            for userid in self.bot.tobekicked[guildid]:
                guild = self.bot.get_guild(guildid)
                member = guild.get_member(userid)
                channel = await self.bot.fetch_channel(self.bot.cache[guild.id]["Logs"])
                try:
                    await member.send(embed=func.Alert(self, member, guild, Language.get(guild.id, self.bot.cache, "AutoMod", "Kicked"), None, Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions")))
                    await guild.kick(member, reason="Watchdog Rules")
                    if channel:
                        await channel.send(embed=func.GoodResponseEmbed(self, guild.id, "{} {}. {}: {}".format(Language.get(guild.id, self.bot.cache, "AutoMod", "Kicked"), member.name, Language.get(guild.id, self.bot.cache, "Moderator", "Reason"), Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions"))))
                    sql.LogMe(guild.id, 7, "{} {}. {}: {}".format(Language.get(guild.id, self.bot.cache, "AutoMod", "Kicked"), member.name, Language.get(guild.id, self.bot.cache, "Moderator", "Reason"), Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions")))
                finally:
                    self.bot.tobekicked[guildid].remove(userid)

    @tasks.loop(seconds=2)
    async def banLoop(self):
        for guildid in self.bot.tobebanned:
            for userid in self.bot.tobebanned[guildid]:
                guild = self.bot.get_guild(guildid)
                member = guild.get_member(userid)
                channel = await self.bot.fetch_channel(self.bot.cache[guild.id]["Logs"])
                try:
                    await member.send(embed=func.Alert(self, member, guild, Language.get(guild.id, self.bot.cache, "AutoMod", "Banned"), None, Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions")))
                    await guild.ban(member, reason="Watchdog Rules", delete_message_days=7)
                    if channel:
                        await channel.send(embed=func.GoodResponseEmbed(self, guild.id, "{} {}. {}: {}".format(Language.get(guild.id, self.bot.cache, "AutoMod", "Banned"), member.name, Language.get(guild.id, self.bot.cache, "Moderator", "Reason"), Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions"))))
                    sql.LogMe(guild.id, 8, "{} {}. {}: {}".format(Language.get(guild.id, self.bot.cache, "AutoMod", "Banned"), member.name, Language.get(guild.id, self.bot.cache, "Moderator", "Reason"), Language.get(guild.id, self.bot.cache, "AutoMod", "TooManyInfractions")))
                finally:
                    self.bot.tobebanned[guildid].remove(userid)

def setup(bot):
    bot.add_cog(Rules(bot))
