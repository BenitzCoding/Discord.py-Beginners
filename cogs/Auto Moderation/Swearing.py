from better_profanity import profanity
from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class SwearFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        text = message.content.replace('*', '')
        censored = profanity.censor(text)
        if '*' in censored:
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Swearing")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][7]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Swearing")))
                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Swearing"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"),member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Swearing")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                await message.delete()
            except:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if not self.Init(after):
            return

        guild = after.guild

        text = after.content.replace('*', '')
        censored = profanity.censor(text)

        if '*' in censored:
            member = after.author
            await after.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(after.guild.id, self.bot.cache, "AutoMod", "Swearing")), delete_after=30)

            if self.bot.cache[after.guild.id]["AutoMod"][7]["Enabled"] == 1:
                if self.bot.cache[after.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[after.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(after.guild.id, self.bot.cache, "AutoMod", "Swearing")))
                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(after.guild.id, self.bot.cache, "AutoMod", "Swearing"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(after.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(after.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(after.guild.id, self.bot.cache, "AutoMod", "Swearing")))
                await Rules.DoRule(self, member, after.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                await after.delete()
            except:
                pass

    def Init(self, message):

        if not message.guild or message.author.bot:
            return

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][7]["Enabled"] < 1:
                return False
        except:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][7]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][7]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        return True

def setup(bot):
    bot.add_cog(SwearFilter(bot))
