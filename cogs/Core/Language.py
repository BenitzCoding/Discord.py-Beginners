import json

from discord.ext import commands

Languages = ["./utils/Translations/English.json",
        "./utils/Translations/Spanish.json",
        "./utils/Translations/German.json",
        "./utils/Translations/English.json", # French
        "./utils/Translations/Dutch.json"]

class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    bot.add_cog(Language(bot))
