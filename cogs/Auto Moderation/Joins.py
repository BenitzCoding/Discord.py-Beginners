from discord.ext import commands, tasks

from utils.functions import func

class MassJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.resetCount.start()

        self.store = {} # Guilds Cache

        self.to_kick = {}

    @tasks.loop(seconds=10)
    async def resetCount(self):
        self.store.clear()

    @tasks.loop(seconds=1)
    async def autoBan(self):
        for guildid in self.to_kick:
            for userid in self.to_kick[guildid]:
                guild = self.bot.get_guild(guildid)
                member = guild.get_member(userid)
                await guild.kick(user=member, reason="Watchdog - Mass Join")
                self.to_kick[guildid].remove(userid)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if not self.Init(member):
            return

        guild = member.guild

        self.store[guild.id]["Count"] += 1

        self.store[guild.id]['Users'].append(member.mention)

        if self.store[guild.id]['Count'] >= self.bot.cache[guild.id]["AutoMod"][6]["Ratelimit"]:
            if self.bot.cache[member.guild.id]["Logs"]:
                channel = await self.bot.fetch_channel(self.bot.cache[member.guild.id]["Logs"])
                await channel.send(embed=func.MassJoinWarning(self, member.guild.id, self.store[guild.id]["Users"]), delete_after=30)

            if self.bot.cache[member.guild.id]["AutoMod"][6]["Enabled"] == 2:
                self.to_kick[member.guild.id].append(member.author.id)

            self.store[guild.id]['Count'] = 0
            self.store[guild.id]['Users'] = []

    def Init(self, member):

        if not member.guild or member.bot:
            return

        try:
            if self.bot.cache[member.guild.id]["AutoMod"][6]["Enabled"] < 1:
                return False
        except:
            return False

        try:
            if not self.bot.cache[member.guild.id]["AutoMod"][6]["Ratelimit"]:
                return False
        except:
            return False


        if not member.guild.id in self.store:
            self.store[member.guild.id] = {"Count": 0, "Users": []}
            self.to_kick[member.guild.id] = []

        return True

def setup(bot):
    bot.add_cog(MassJoin(bot))
