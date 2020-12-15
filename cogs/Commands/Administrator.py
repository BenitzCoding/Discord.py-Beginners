import os

from discord.ext import commands

from utils.functions import func
from utils import sql

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_data(self, ctx):
        if ctx.author.id != 439327545557778433:
            return

        servers = self.bot.guilds

        for i in servers:
            sql.AddData(i.id)
            print(f"Added {i.id}")

    @commands.command()
    async def reload(self, ctx):
        if ctx.author.id != 439327545557778433:
            return

        dirs = ["cogs/Auto Moderation", "cogs/Commands", "cogs/Core", "utils"]

        for directory in dirs:
            for file in os.listdir(directory):
                if file.endswith(".py") and file != "__pycache__" and file != "sql.py":
                    directory = directory.replace("/", ".")
                    self.bot.unload_extension(f"{directory}.{file[:-3]}")
                    self.bot.load_extension(f"{directory}.{file[:-3]}")

        await ctx.author.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "Reloaded everything"))

    @commands.command()
    async def count(self, ctx):
        if ctx.author.id != 439327545557778433:
            return

        await ctx.author.send(len(self.bot.guilds))

def setup(bot):
    bot.add_cog(Admin(bot))
