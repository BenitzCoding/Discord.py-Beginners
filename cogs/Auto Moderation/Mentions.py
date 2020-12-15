from discord.ext import commands, tasks

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class MassMention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.resetCount.start()

        self.store = {} # Guilds Cache

    @tasks.loop(seconds=10)
    async def resetCount(self):
        self.store.clear()

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        mentions = len(message.mentions)

        self.store[message.guild.id][message.author.id] += int(mentions)

        if self.store[guild.id][message.author.id] >= self.bot.cache[guild.id]["AutoMod"][2]["Ratelimit"]:
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Mentions")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][2]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id,member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Mentions")))

                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Mentions"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Mentions")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                msgs = []

                async for messagea in message.channel.history(limit=self.bot.cache[guild.id]["AutoMod"][2]["Ratelimit"]):
                    if member == messagea.author:
                        if len(messagea.mentions) > 0:
                            msgs.append(messagea)

                await message.channel.delete_messages(msgs)
                msgs.clear()
            except:
                pass

            self.store[guild.id][member.id] = 0

    def Init(self, message):

        if not message.guild or message.author.bot:
            return False

        if not message.mentions:
            return False

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][2]["Enabled"] < 1:
                return False
        except:
            return False

        if not self.bot.cache[message.guild.id]["AutoMod"][2]["Ratelimit"]:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][2]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][2]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        if not message.guild.id in self.store:
            self.store[message.guild.id] = {}

        if not message.author.id in self.store[message.guild.id]:
            self.store[message.guild.id][message.author.id] = 0



        return True

def setup(bot):
    bot.add_cog(MassMention(bot))
