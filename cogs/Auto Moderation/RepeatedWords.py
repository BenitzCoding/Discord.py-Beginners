import discord

from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class RepeatedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.store = {}

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        self.store[guild.id][message.author.id]['Percentage'] = 0
        self.store[guild.id][message.author.id]['String'] = list(message.content.lower().split())

        self.store[guild.id][message.author.id]['Unique'] = []
        for i in self.store[guild.id][message.author.id]['String']:
            if not i in self.store[guild.id][message.author.id]['Unique']:
                self.store[guild.id][message.author.id]['Unique'].append(i)

        self.store[guild.id][message.author.id]['Percentage'] = (len(self.store[guild.id][message.author.id]['Unique']) / len(message.content.lower().split()) * 100)

        if self.store[guild.id][message.author.id]['Percentage'] >= self.bot.cache[guild.id]["AutoMod"][1]["Ratelimit"]:
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Repeated")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][1]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Repeated")))
                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Repeated"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Repeated")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                await message.delete()
            except:
                pass

                self.store[guild.id][message.author.id]['Percentage'] = 0
                self.store[guild.id][message.author.id]['String'] = None
                self.store[guild.id][message.author.id]['Unique'] = []

    def Init(self, message):

        if not message.guild or message.author.bot:
            return False

        if not len(list(message.content.lower().split())) > 10:
            return False

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][1]["Enabled"] < 1:
                return False
        except:
            return False

        if not self.bot.cache[message.guild.id]["AutoMod"][1]["Ratelimit"]:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][1]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][1]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        if not message.guild.id in self.store:
            self.store[message.guild.id] = {}

        if not message.author.id in self.store[message.guild.id]:
            self.store[message.guild.id][message.author.id] = {"String": None, "Percentage": 0, "Unique": []}

        return True


def setup(bot):
    bot.add_cog(RepeatedWords(bot))
