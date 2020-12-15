from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

class FileExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.store = {}

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        filetypes = ['.exe', '.py', '.dll', '.xls', '.doc', '.xlsx', '.docx', '.vbs', '.sln', '.application', '.com', '.cpl']

        for i in message.attachments:
            for f in filetypes:
                j = i.filename.lower()
                if j.endswith(f):
                    self.store[guild.id] = True

        if self.store[guild.id] == True:
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "File")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][9]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "File")))

                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "File"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "File")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                await message.delete()
            except:
                pass
            self.store[guild.id] = False

    def Init(self, message):

        if not message.guild or message.author.bot:
            return

        if not len(message.attachments) > 0:
            return

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][9]["Enabled"] < 1:
                return False
        except:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][9]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][9]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        if not message.guild.id in self.store:
            self.store[message.guild.id] = False

        return True

def setup(bot):
    bot.add_cog(FileExt(bot))
