import re

from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class MassEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.store = {} # Guilds Cache

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        self.store[guild.id][message.author.id]["String"] = message.content
        self.store[guild.id][message.author.id]["Count"] = 0
        self.store[guild.id][message.author.id]["Count"] = len(re.findall(u'[\U00010000-\U0010ffff]', message.content)) # Normal Emojis
        self.store[guild.id][message.author.id]["Count"] += len(re.findall('<(?P<animated>a)?:(?P<name>[0-9a-zA-Z_]{2,32}):(?P<id>[0-9]{15,21})>', message.content)) # Custom Emojis

        if self.store[guild.id][message.author.id]["Count"] > self.bot.cache[guild.id]["AutoMod"][4]["Ratelimit"]:
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Emojis")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][4]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Emojis")))

                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Emojis"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Emojis")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                await message.delete()
            except:
                pass

            self.store[guild.id][member.id]['Count'] = 0
            self.store[guild.id][member.id]['String'] = None

    def Init(self, message):

        if not message.guild or message.author.bot:
            return

        if len(message.content) <= 5:
            return

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][4]["Enabled"] < 1:
                return False
        except:
            return False

        if not self.bot.cache[message.guild.id]["AutoMod"][4]["Ratelimit"]:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][4]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][4]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        if not message.guild.id in self.store:
            self.store[message.guild.id] = {}

        if not message.author.id in self.store[message.guild.id]:
            self.store[message.guild.id][message.author.id] = {"String": None, "Count": 0}

        return True

def setup(bot):
    bot.add_cog(MassEmoji(bot))
