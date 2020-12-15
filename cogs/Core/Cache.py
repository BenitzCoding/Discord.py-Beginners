import json

from discord.ext import commands

from utils import sql

Languages = ["./utils/Translations/English.json",
        "./utils/Translations/Spanish.json",
        "./utils/Translations/German.json",
        "./utils/Translations/English.json", # French
        "./utils/Translations/Dutch.json"]

class Cache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message_cache(self, message):
        if not message.guild:
            return

        if not message.guild.id in self.bot.cache:
            self.bot.cache[message.guild.id] = sql.Cache(message.guild.id)

        if message.guild.id in self.bot.cache:  # Updates cache if it is different from the current one
            Settings = sql.Cache(message.guild.id)

            if Settings != self.bot.cache[message.guild.id]:
                self.bot.cache[message.guild.id] = Settings
        return

    def get(ID, cache, *args):
        try:
            toOpen = Languages[cache[ID]["Language"]]
            with open(toOpen) as f:
                language = json.load(f)

            amount = len(args)
            if amount == 1:
                return language[args[0]]

            if amount == 2:
                return language[args[0]][args[1]]

            if amount == 3:
                return language[args[0]][args[1]][args[2]]
        except:
            return

def setup(bot):
    bot.add_cog(Cache(bot))
