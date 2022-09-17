from datetime import datetime 

import discord
from discord.ext import commands
import asyncio


class ssu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members = True)
    @commands.has_role('Staff')
    async def ssu(self, ctx):
      channel = self.bot.get_channel(914524652347490334)
      title = "Server Start Up"
      descrip = "Hi, there is a Server Start up now,come along and have some fun! \n\n https://www.roblox.com/games/5958752687/Perthshire-Scotland"
 
      embed = discord.Embed(title=title, description =descrip,timestamp=ctx.message.created_at)

      embed.add_field(name='SSU Host:', value=ctx.author.mention)
   
    
    

      await ctx.message.delete()
      await ctx.author.send(f"{ctx.author.mention} your SSU has succesfully been posted.")
      await channel.send("@here")
      await channel.send(embed =embed)
    
    @commands.command()
    @commands.guild_only()
    async def mods(self, ctx):
        """ Check which mods are online on current guild """
        message = ""
        all_status = {
            "online": {"users": [], "emoji": "🟢"},
            "idle": {"users": [], "emoji": "🟡"},
            "dnd": {"users": [], "emoji": "🔴"},
            "offline": {"users": [], "emoji": "⚫"}
        }

        for user in ctx.guild.members:
            user_perm = ctx.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(f"**{user}**")

        for g in all_status:
            if all_status[g]["users"]:
                message += f"{all_status[g]['emoji']} \n{', '.join(all_status[g]['users'])}\n"

        await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")
    
    @commands.command()
    @commands.guild_only()
    async def joinedat(self, ctx, *, user: discord.Member = None):
        """ Check when a user joined the current server """
        user = user or ctx.author
        des = f"**{user}** joined **{ctx.guild.name}**\n{user.joined_at}"

        embed = discord.Embed(description=des)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def server_banner(self, ctx):
        """ Get the current banner image """
        if not ctx.guild.banner:
            return await ctx.send("This server does not have a banner... :sob:")
        await ctx.send(f"Banner of **{ctx.guild.name}**\n{ctx.guild.banner.with_format('png')}")
    

    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.User = None, *, reason=None):
        """
        Bans a user from the server.
        """
        if member == None or member == ctx.message.author:
            await ctx.channel.send("Friendly reminder you're dumb trying to ban yourself mwah!")
            return
        if reason == None:
            reason = "Reason was not specified"

        embed = discord.Embed(
            title="",
            timestamp=datetime.utcnow(),
        )
        embed.add_field(name="successful", value=f"{member.mention} has been banned for {reason}")
        embed.set_footer(text=f"{ctx.message.author.name}")

        await ctx.send(embed=embed)
        await ctx.guild.ban(member, reason=reason)
    
    @commands.command()
    @commands.has_guild_permissions(ban_members = True)
    async def unban(self,ctx, *, member):
        """|| Unban command no need of mention use like Expressingames#2342"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=None):
        """Purge an amount of messages in a channel
        -------------------------
        Ex:
        c?purge 50"""
        if amount is None:
            return await ctx.send('Hey, please do `.purge [amount]`!')
        if amount>500 or amount<0:
            return await ctx.send('Invalid amount. Maximum is 500')
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=amount)
        chan1 = self.bot.get_channel(881640389126271006)
        description = f"Sucesfully deleted **{int(amount)}** messages!"
        embed = discord.Embed(description=description)
        embed.add_field(name="User", value=ctx.author, inline=True)
        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
        await chan1.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages = True)
    async def announce2(self,ctx, chan: discord.TextChannel, * , announcement=None):
        """|| announces something """
        if not announcement:
            await ctx.send("provide a announcement")
        await chan.send(f'{announcement}')

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages = True)
    async def dm(self,ctx, member: discord.Member, * , text=None):
        await member.send(f"{text}")
        await ctx.send(f"{member} was sent a DM by {ctx.author} with the message :``` {text} ```")

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages = True)
    async def announce(self,ctx, chan: discord.TextChannel, * , announcement=None):
        """|| announces something """
        if not announcement:
            await ctx.send("provide a announcement")
        colour = discord.Colour.from_rgb(239, 162, 144)
        embed = discord.Embed(colour = colour, timestamp=ctx.message.created_at)
        embed.add_field(name="Announcement" , value=announcement)
        embed.set_footer(text=f"Sent by {ctx.author}")
        await chan.send(embed=embed)
        await ctx.reply(f"Successfully sent the announcement to {chan.mention}!")
    
   
   
def setup(bot):
    bot.add_cog(ssu(bot))
