import re

from discord.ext import commands, tasks

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class MassSpoiler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.resetCount.start()

        self.store = {}

    @tasks.loop(seconds=10)
    async def resetCount(self):
        self.store.clear()

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        spoilers = re.findall(r"\|{2}([\w ]+)\|{2}", message.content)

        if len(spoilers) > 0:
            self.store[guild.id][message.author.id]["Count"] += len(spoilers)
            self.store[guild.id][message.author.id]["Messages"].append(message.id)

        if self.store[guild.id][message.author.id]["Count"] >= self.bot.cache[guild.id]["AutoMod"][10]["Ratelimit"]:
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Spoilers")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][10]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Spoilers")))
                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Spoilers"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Spoilers")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                msgs = []

                async for messagea in message.channel.history(limit=self.bot.cache[guild.id]["AutoMod"][10]["Ratelimit"]):
                    if member == messagea.author:
                        msgs.append(messagea)

                await message.channel.delete_messages(msgs)
                msgs.clear()
            except:
                pass

            try:
                self.store[guild.id][member.id]["Count"] = 0
                self.store[guild.id][member.id]["Messages"].clear()
            except:
                return

    def Init(self, message):
        if not message.guild or message.author.bot:
            return

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][10]["Enabled"] < 1:
                return False
        except:
            return False

        if not self.bot.cache[message.guild.id]["AutoMod"][10]["Ratelimit"]:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][10]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][10]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        if not message.guild.id in self.store:
            self.store[message.guild.id] = {}

        if not message.author.id in self.store[message.guild.id]:
            self.store[message.guild.id][message.author.id] = {"Count": 0, "Messages": []}

        return True

def setup(bot):
    bot.add_cog(MassSpoiler(bot))
