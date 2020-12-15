import datetime
import discord
import random
import json
import os

from discord.ext import commands
from collections import namedtuple
from cogs.Core.Language import Language

def fetch(file):
    try:
        with open(file, encoding="utf8") as data:
            return json.load(data, object_hook=lambda d: namedtuple("X", d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

def boot():
    os.remove("./data/sniper.json")
    data = open("./data/sniper.json", "w+")
    data.write("{}")
    data.close()

class func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def NoPerm(self, id):
        title = random.choice(Language.get(id, self.bot.cache, "BadResponses"))
        embed = discord.Embed(
            title = title,
            description = Language.get(id, self.bot.cache, "Functions", "NoPerm"),
            colour = 0xebc634,
            timestamp=datetime.datetime.utcnow()
            )

        return embed

    def ErrorEmbed(self, id, error):
        title = random.choice(Language.get(id, self.bot.cache, "ErrorResponses"))
        embed = discord.Embed(
            title = title,
            description = error,
            colour = 0xebc634,
            timestamp=datetime.datetime.utcnow()
            )

        return embed

    def BadResponseEmbed(self, id, desc):
        title = random.choice(Language.get(id, self.bot.cache, "BadResponses"))
        embed = discord.Embed(
            title = title,
            description = desc,
            colour = 0xebc634,
            timestamp=datetime.datetime.utcnow()
            )
        return embed

    def GoodResponseEmbed(self, id, desc):
        title = random.choice(Language.get(id, self.bot.cache, "GoodResponses"))
        embed = discord.Embed(
            title = title,
            description = desc,
            colour = 0x27b1db,
            timestamp=datetime.datetime.utcnow()
            )
        return embed

    def AutoModInfraction(self, Guild, User, InfractionsCount, Reason):
        embed = discord.Embed(
            colour=0x27b1db,
            description="**{}:** {}\n**{}:** Watchdog".format(Language.get(Guild.id, self.bot.cache,"AutoMod", "Reason"), Reason, Language.get(Guild.id, self.bot.cache, "Functions", "Invoker"))
            )
        embed.set_author(name="{}#{} {}".format(User.name, User.discriminator, Language.get(Guild.id, self.bot.cache, "Functions", "Recieved")))
        embed.set_footer(text="{}: {}".format(Language.get(Guild.id, self.bot.cache, "Functions", "UInfractions"), InfractionsCount))

        return embed

    def MassJoinWarning(self, id, users):
        embed = discord.Embed(
            colour=0x27b1db,
            description="**{}:\n\n{}**".format(Language.get(id, self.bot.cache, "Functions", "UsersInvolved"), "\n ".join(users))
            )
        embed.set_author(name=Language.get(id, self.bot.cache, "Functions", "MassJoinWarning"))
        embed.set_footer(text="{}: {}".format(Language.get(id, self.bot.cache, "Functions", "Users"), len(users)))

        return embed

    def Alert(self, User, Guild, Action, Invoker=None, Reason=None, Duration=None):

        embed = discord.Embed(title="{}, {}!".format(Language.get(Guild.id, self.bot.cache, "Functions", "Hey"), User.name),
            colour=0x27b1db,
            description="{} {}!".format(Language.get(Guild.id, self.bot.cache, "Functions", "Action"), Action)
        )
        embed.set_author(name=Guild.name, icon_url=Guild.icon_url)
        if Invoker:
            embed.add_field(name=Language.get(Guild.id, self.bot.cache, "Functions", "By"), value=Invoker, inline=True)
        if Reason:
            embed.add_field(name=Language.get(Guild.id, self.bot.cache, "Functions", "Reason"), value=Reason, inline=True)
        if Duration:
            embed.add_field(name=Language.get(Guild.id, self.bot.cache, "Functions", "Duration"), value=Duration, inline=True)

        return embed

def setup(client):
    client.add_cog(func(client))
