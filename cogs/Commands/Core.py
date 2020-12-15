import discord
import os

from discord.ext import commands

from utils.functions import func
from cogs.Core.Language import Language
from utils import sql

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def help(self, ctx):
        embed = discord.Embed(colour=0x27b1db)
        embed.set_author(name="Watchdog - {}".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "Help")))
        embed.set_footer(text=Language.get(ctx.guild.id, self.bot.cache, "Core", "HelpFooter"))
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Core", "AutoMod"), value=f"`{ctx.prefix}help automod`", inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Core", "Mod"), value=f"`{ctx.prefix}help moderator`", inline=True)
        embed.add_field(name=Language.get(ctx.guild.id, self.bot.cache, "Core", "Commands"), value=f"`{ctx.prefix}help commands`", inline=True)

        await ctx.send(embed=embed)

    @help.group(invoke_without_command=True, name="automod")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def automod_(self, ctx):
        desc = f"""
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "AutoModDesc")}
        
        [{Language.get(ctx.guild.id, self.bot.cache, "Core", "Dashboard")}](https://watchdogbot.net/)
        """

        embed = discord.Embed(description=desc, colour=0x27b1db)
        embed.set_author(name="Watchdog - {}".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "AutoMod")))
        await ctx.send(embed=embed)

    @help.group(invoke_without_command=True, name="moderator")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def moderator_(self, ctx):
        desc = f"""
        `{ctx.prefix}kick #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")} ({Language.get(ctx.guild.id, self.bot.cache, "Core", "Reason")})`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Kick")}

        `{ctx.prefix}ban #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")} ({Language.get(ctx.guild.id, self.bot.cache, "Core", "Reason")})`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Ban")}

        `{ctx.prefix}clear [{Language.get(ctx.guild.id, self.bot.cache, "Core", "Amount")}]`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Clear")}

        `{ctx.prefix}mute #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")} [{Language.get(ctx.guild.id, self.bot.cache, "Core", "Duration")}]`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Mute")}

        `{ctx.prefix}unmute #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")}`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Unmute")}

        `{ctx.prefix}warn #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")} ({Language.get(ctx.guild.id, self.bot.cache, "Core", "Reason")})`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Warn")}

        `{ctx.prefix}infractions remove #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")} [{Language.get(ctx.guild.id, self.bot.cache, "Core", "WarnID")}]`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Unwarn")}

        `{ctx.prefix}infractions #{Language.get(ctx.guild.id, self.bot.cache, "Core", "User")}`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Infractions")}

        `{ctx.prefix}snipe `
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Snipe")}

        `{ctx.prefix}say [{Language.get(ctx.guild.id, self.bot.cache, "Core", "Words")}]`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Say")}
        """

        embed = discord.Embed(description=desc, colour=0x27b1db)
        embed.set_author(name="Watchdog - {}".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "Mod")))
        await ctx.send(embed=embed)

    @help.group(invoke_without_command=True, name="commands")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    async def commands_(self, ctx):
        desc = f"""
        `{ctx.prefix}invite`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Invite")}

        `{ctx.prefix}vote`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Vote")}

        `{ctx.prefix}serverinfo`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Sinfo")} `{ctx.prefix}sinfo`

        `{ctx.prefix}userinfo`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Uinfo")} `{ctx.prefix}uinfo`

        `{ctx.prefix}roleinfo [role]`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Rinfo")} `{ctx.prefix}rinfo [{Language.get(ctx.guild.id, self.bot.cache, "Core", "Role")}]`

        `{ctx.prefix}botinfo`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Binfo")} `{ctx.prefix}binfo, {ctx.prefix}info`
        
        `{ctx.prefix}spotify`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "Spotify")}
        
        `{ctx.prefix}requestdata`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "RD")}

        `{ctx.prefix}dashboard`
        {Language.get(ctx.guild.id, self.bot.cache, "Core", "DashHelp")}
        """

        embed = discord.Embed(description=desc, colour=0x27b1db)
        embed.set_author(name="Watchdog - {}".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "Commands")))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 604800, commands.BucketType.user)
    async def requestdata(self, ctx):
        sql.GetData(ctx.author.id)
        file = discord.File(f'./{ctx.author.id}-datarequest.txt', filename=f"{ctx.author.id}-data.txt")

        if file:
            await ctx.author.send("Here", file=file, delete_after=120)
            os.remove(f"./{ctx.author.id}-datarequest.txt")
        else:
            await ctx.author.send("There is no data stored about you.")

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.guild_only()
    async def setup(self, ctx):
        muted_role = discord.utils.get(ctx.guild.roles, name="muted")

        if not muted_role:
            try:
                role = await ctx.guild.create_role(name="muted")
            except:
                return await ctx.author.send(embed=func.BadResponseEmbed(self, ctx.guild.id, "{} {}setup @ {}".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "Error", "CantCreateMutedRole"), ctx.prefix, ctx.guild.name)))

        Failed = []
        for channel in ctx.guild.channels:
            if channel.type != "voice":
                if not channel.overwrites_for(muted_role):
                    try:
                        await channel.set_permissions(role, send_messages=False, add_reactions=False)
                    except:
                        Failed.append(channel.name)
                        pass

        if len(Failed) > 0:
            return await ctx.author.send(embed=func.BadResponseEmbed(self, ctx.guild.id, "{}\n\n {}".format(Language.get(ctx.guild.id, self.bot.cache, "Errors", "CantSetOverwrite"), "\n".join(Failed))))

        await ctx.author.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "{} {}!".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "SetupComplete"), ctx.guild.name)))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vote(self, ctx):
        await ctx.author.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "[{}](https://top.gg/bot/702141833437773824)".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "Clickme"))))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        await ctx.author.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "[{}](https://discord.com/oauth2/authorize?client_id=702141833437773824&scope=bot&permissions=268528662)".format(Language.get(ctx.guild.id, self.bot.cache, "Core", "Clickme"))))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dashboard(self, ctx):
        await ctx.author.send(embed=func.GoodResponseEmbed(self, ctx.guild.id, "[{}](https://watchdogbot.net/)".format(
            Language.get(ctx.guild.id, self.bot.cache, "Core", "Clickme"))))

def setup(bot):
    bot.add_cog(Core(bot))
