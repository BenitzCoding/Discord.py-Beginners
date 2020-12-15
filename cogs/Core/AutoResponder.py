import discord
import asyncio
import json

from discord.ext import commands

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./data/AutoResponder.json") as f:
            self.responses = json.load(f)

    @commands.Cog.listener(name="on_message")
    async def on_message_(self, message):

        if message.guild != None:
            return

        await asyncio.sleep(3) # Ratelimiting Countermeasure

        await self.DMLog(message)

        if message.author.bot:
            return

        for response in self.responses:
            if response in message.content.lower():
                return await message.author.send(self.responses[response])

    async def DMLog(self, message):
        try:
            dmschan = await self.bot.fetch_channel(705957507557884006)
            if message.content and message.content != '':
                if message.author != self.bot.user:
                    await dmschan.send(embed=self.Embed("User Message", message.content))
                else:
                    await dmschan.send(embed=self.Embed("Bot Response", message.content))
        except:
            return

    def Embed(self, author, description):
        embed = discord.Embed(
                description = description,
                colour = 0xc70300
                )
        embed.set_author(name=author)

        return embed

def setup(bot):
    bot.add_cog(AutoResponder(bot))
