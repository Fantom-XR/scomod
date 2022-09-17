import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from discord_components import DiscordComponents, Button
from ro_py import Client
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
from dotenv import load_dotenv
import os
import random
import utils
import aiohttp
import aiofiles
import keep_alive
import asyncio
from better_profanity import profanity


load_dotenv()  # Load environment variables from .env file.


bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents=discord.Intents.all())
bot.remove_command("help")
bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}

#roblox = Client(os.getenv("COOKIE"))
    

@bot.event
async def on_ready():
    for guild in bot.guilds:
        bot.warnings[guild.id] = {}
        
        async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
            pass

        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]
    
    DiscordComponents(bot)
    print(bot.user.name + " is ready.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Scotland™ Members"))  

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

#@bot.command(pass_context=True)
#async def role(ctx, user: discord.Member, role: discord.Role):
    #await user.remove_roles(role)
    #await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

@bot.command()
async def afk(ctx, mins):
    current_nick = ctx.author.nick
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes.")
    await ctx.author.edit(nick=f"{ctx.author.name} [AFK]")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)

        if counter == int(mins):
            await ctx.author.edit(nick=current_nick)
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            break
            
@bot.command()
@commands.has_permissions(manage_messages = True)
async def warn(ctx, member: discord.Member=None, *, reason=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
        
    if reason is None:
        return await ctx.send("Please provide a reason for warning this user.")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = bot.warnings[ctx.guild.id][member.id][0]

    async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

@bot.command()
@commands.has_permissions(manage_messages = True)
async def warnings(ctx, member: discord.Member=None):
    if member is None:
        return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
    embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: # no warnings
        await ctx.send("This user has no warnings.")


@bot.command()
async def ping(ctx):
    """|| Tells the bot's latency """
    await ctx.send(f"{round(bot.latency * 1000)} ms")

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")


    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmutedd from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.blue()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

  await ctx.send(embed=embed)
    
@bot.event
async def on_member_join(member):
    chan1 = member.guild.get_channel(873931671521611807)
    colour = discord.Colour.from_rgb(255, 255, 255)
    title = "New Member!"
    description = f"Welcome to Newcastle,{member.mention}! We wish you a great time in our community."
    embed = discord.Embed(colour = colour, title=title, description=description)
    embed.set_thumbnail(url=f"{member.avatar_url}")
    #embed.set_image(url="https://www.fantomxr.cf/imgs/AVwelcome.png")
    await chan1.send(embed=embed)

    name1 = (f"Member Count : {member.guild.member_count}")
    chan = member.guild.get_channel(873939611007737856)
    await chan.edit(name=name1)


@bot.command(pass_context=True)
async def update_member_count(ctx):
    while True:
        await ctx.send(ctx.guild.member_count)
        channel = discord.utils.get(ctx.guild.channels, id=911591413383319562)
        await channel.edit(name=f'Member Count: {ctx.guild.member_count}')
        await asyncio.sleep(120)


@bot.command()
async def updatem(ctx):
    bot.loop.create_task(update_member_count(ctx))  # Create loop/task
    await ctx.send("Loop started, changed member count.") # Optional


@bot.command()
async def whois(ctx, *, user: discord.Member = None):
	if user is None:
		user = ctx.author
	date_format = "%a, %d %b %Y %I:%M %p"
	embed = discord.Embed(color=0xdfa3ff, description=user.mention)
	embed.set_author(name=str(user), icon_url=user.avatar_url)
	embed.set_thumbnail(url=user.avatar_url)
	embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
	members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
	embed.add_field(name="Join position", value=str(members.index(user) + 1))
	embed.add_field(name="Registered",
	                value=user.created_at.strftime(date_format))
	if len(user.roles) > 1:
		role_string = ' '.join([r.mention for r in user.roles][1:])
		embed.add_field(name="Roles [{}]".format(len(user.roles) - 1),
		                value=role_string,
		                inline=False)
	perm_string = ', '.join([
	    str(p[0]).replace("_", " ").title() for p in user.guild_permissions
	    if p[1]
	])
	embed.add_field(name="Guild permissions", value=perm_string, inline=False)
	embed.set_footer(text='ID: ' + str(user.id))
	return await ctx.send(embed=embed)

"""@bot.command()
@commands.guild_only()
@commands.has_role('Staff')
async def ssu(ctx):
 
    channel = bot.get_channel(884496869894524999)
    title = "Server Start Up"
    descrip = "Hi, there is a Server Start up now come along and have some fun! \n\n https://www.roblox.com/games/6794843414/Newcastle-England"
 
    embed = discord.Embed(title=title, description =descrip,timestamp=ctx.message.created_at)

    embed.add_field(name='SSU Host:', value=ctx.author.mention)
   
    
    

    await ctx.message.delete()
    await ctx.author.send(f"{ctx.author.mention} your SSU has succesfully been posted.")
    await channel.send("@here")
    await channel.send(embed =embed)"""
 

#link to group

@bot.command()
async def group(ctx):
    """|| Gives you link the the group!"""
    await ctx.send("https://www.roblox.com/groups/4170430")

@bot.command()
async def mb(ctx):
    await ctx.send(f"There are {ctx.guild.member_count} members in the server!")

bot.load_extension("COgs.help")
bot.load_extension("COgs.moderaion")
bot.load_extension("COgs.logstaff")
bot.load_extension("COgs.auto")
bot.load_extension("COgs.fun")
#bot.load_extension("COgs.ai_moderation")
bot.run(os.getenv("TOKEN"))
