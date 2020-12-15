import aiohttp
import re

from discord.ext import commands

from utils import sql
from utils.functions import func
from cogs.Core.Rules import Rules
from cogs.Core.Language import Language

INVITE_RE = (
    r"(?:discord(?:[\.,]|dot)gg|"                     # Could be discord.gg/
    r"discord(?:[\.,]|dot)com(?:\/|slash)invite|"     # or discord.com/invite/
    r"discordapp(?:[\.,]|dot)com(?:\/|slash)invite|"  # or discordapp.com/invite/
    r"discord(?:[\.,]|dot)me|"                        # or discord.me
    r"discord(?:[\.,]|dot)io"                         # or discord.io.
    r")(?:[\/]|slash)"                                # / or 'slash'
    r"([a-zA-Z0-9]+)"                                 # the invite code itself
)

class ServerInvites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.Init(message):
            return

        guild = message.guild

        if await self.invite_codes(message):
            member = message.author
            await message.channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Invites")), delete_after=30)

            if self.bot.cache[message.guild.id]["AutoMod"][5]["Enabled"] == 1:
                if self.bot.cache[message.guild.id]["Logs"]:
                    channel = await self.bot.fetch_channel(self.bot.cache[message.guild.id]["Logs"])
                    await channel.send(embed=func.AutoModInfraction(self, guild, member, len(sql.GetInfractions(guild.id, member.id)), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Invites")))

                sql.Warn(guild.id, member.id, 702141833437773824, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Invites"))
                sql.LogMe(guild.id, 9, "{} {}. {}: {}".format(Language.get(message.guild.id, self.bot.cache, "AutoMod", "Warned"), member.name, Language.get(message.guild.id, self.bot.cache, "AutoMod", "Reason"), Language.get(message.guild.id, self.bot.cache, "AutoMod", "Invites")))
                await Rules.DoRule(self, member, message.guild, self.bot.tobemuted, self.bot.tobekicked, self.bot.tobebanned)

            try:
                await message.delete()
            except:
                pass


    def Init(self, message):
        if not message.guild or message.author.bot:
            return

        try:
            if self.bot.cache[message.guild.id]["AutoMod"][5]["Enabled"] < 1:
                return False
        except:
            return False

        if self.bot.cache[message.guild.id]["AutoMod"][5]["Ignored"] and str(message.channel.id) in self.bot.cache[message.guild.id]["AutoMod"][5]["Ignored"]:
            return False

        if self.bot.cache[message.guild.id]["IgnoredRoles"]:
            for role in message.author.roles:
                if str(role.id) in self.bot.cache[message.guild.id]["IgnoredRoles"]:
                    return False

        return True

    async def invite_codes(self, text):
        words = text.content.replace("\\", "")

        invites = re.findall(INVITE_RE, words, re.IGNORECASE)
        for invite in invites:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://discordapp.com/api/invites/{invite}') as r:
                    response = await r.json()
                    guild = response.get("guild")
                    if guild:
                        if int(guild['id']) != text.guild.id:
                            return True
        return False

def setup(bot):
    bot.add_cog(ServerInvites(bot))
