import discord
from discord.ext import commands
from discord.enums import ActivityType, Status
from types import SimpleNamespace

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        colour = discord.Colour.from_rgb(54, 57, 62)
        embed = discord.Embed(colour = colour, timestamp = ctx.message.created_at)
        embed.set_author(name="Commands")


        embed.add_field(name = ".help", value="Shows a list of all commands.", inline=False)
        embed.add_field(name = ".ping", value="Test our server speed.", inline=False)
        embed.add_field(name = ".group ", value="Gives a link to our Roblox Group.", inline=False)
        embed.add_field(name = ".userinfo", value=".userinfo [ @User ]", inline=False)
        embed.add_field(name = ".serverinfo", value=".serverinfo", inline=False)
        embed.add_field(name = ".ban" , value = ".ban [ User - Do not @ ] [ Reason(s) ]", inline=False)
        embed.add_field(name = ".unban" , value = ".unban [ User - Do not @ ]", inline=False)
        embed.add_field(name = ".kick" , value = ".kick [ User - Do not @ ] [ Reason(s) ]", inline=False)
        embed.add_field(name = ".announce" , value = ".announce [ #channel ] [ Message ] - Embedded", inline=False)
        embed.add_field(name = ".announce2 " , value = ".announce2 [ #channel ] [ Message ] - Text")
        embed.add_field(name = ".purge" , value = ".purge [ Number of Messages ]", inline=False)
        embed.add_field(name = ".dm" , value = ".dm [ @User ] [ Message ]", inline=False)
        embed.add_field(name = ".warn" , value = ".warn [ @User ] [ Reason ]", inline=False)
        embed.add_field(name = ".warnings" , value = ".warnings [ @User ]", inline=False)
        embed.add_field(name = ".mb" , value="Member Count" , inline=False)
        embed.add_field(name = ".eightball" , value=".eightball [ Question ]" , inline=False)
        embed.add_field(name = ".mods" , value="Gives list of mods in server." , inline=False)
        embed.add_field(name = ".f" , value="Press F to pay respect!" , inline=False)
        embed.add_field(name = ".reverse" , value=".reverse [ message ]" , inline=False)
        embed.add_field(name = ".password" , value="Generates a random password string for you. This returns a random URL-safe text string, containing nbytes random bytes. The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.!" , inline=False)
        embed.add_field(name = ".rate" , value=".rate [ Thing ]" , inline=False)
        embed.add_field(name = ".beer" , value=".beer [ @user ]" , inline=False)
        embed.add_field(name = ".hotcalc" , value=".hotcalc [ @user ]" , inline=False)
        embed.add_field(name = ".slot" , value="Roll the slot machine." , inline=False)
        embed.add_field(name = ".addprofanity" , value=".addprofanity [ Profanity ]" , inline=False)
        embed.add_field(name = ".delprofanity" , value=".delprofanity [ Profanity ]" , inline=False)
        embed.set_footer(text=f"All commands have . as prefix")

        await ctx.author.send(embed=embed)
        await ctx.reply("**Please check your DMs!**")
def setup(bot):
    bot.add_cog(Help(bot))
