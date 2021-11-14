import discord
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from discord_components import DiscordComponents, Button
from ro_py import Client
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
from dotenv import load_dotenv
import os
import random
import aiofiles
import keep_alive

load_dotenv()  # Load environment variables from .env file.


bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), case_insensitive=True, intents=discord.Intents.all())
bot.remove_command("help")
bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}

roblox = Client(os.getenv("COOKIE"))
    

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Avenir"))  

@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}

#@bot.command(pass_context=True)
#async def role(ctx, user: discord.Member, role: discord.Role):
    #await user.remove_roles(role)
    #await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

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
    chan1 = member.guild.get_channel(790682463126945792)
    colour = discord.Colour.from_rgb(255, 255, 255)
    title = "New Member!"
    description = f"Welcome to Avenir,{member.mention}! We wish you a great time in our server."
    embed = discord.Embed(colour = colour, title=title, description=description)
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_image(url="https://www.fantomxr.cf/imgs/AVwelcome.png")
    await chan1.send(embed=embed)

@bot.event
async def on_member_join(member):
    title = "New Member!"
    description = "Please read below to get started."
    embed = discord.Embed(title=title, description=description)
    embed.set_author(name=f"Welcome! {member.name}", icon_url=f"{member.guild.icon_url}")
    embed.add_field(name="Rules", value="Please make sure to read over the rules and guidelines within the Avenir discord to ensure we can sustain a better and more suitable environment for our server and community. Disobey these rules and you can be subject to being banned.", inline=False)
    embed.add_field(name="Ordering and Purchasing", value="If you wish to purchase a Avenir product please head for the #information channel or say .hub to find our Purchase Centre for you to get started", inline=False)
    embed.set_footer(text="We hope you enjoy your time here at Avenir.", icon_url=f"{member.guild.icon_url}")
    await member.send(embed=embed)

@bot.command()
async def userinfo(ctx, *, user: discord.Member = None):
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
async def suggest(ctx, *, message=None):
    if not message:
        await ctx.send("Please Introduce a suggestion :/.")
        return
 
    channel = bot.get_channel(788520182549053472)
    message = message
 
    embed = discord.Embed(timestamp=ctx.message.created_at)

    embed.set_author(name='New Suggestion!')

    embed.add_field(name='Suggestion By:', value=ctx.author.mention)
    embed.add_field(name='Suggestion:', value=message)
   
    
    

    await ctx.message.delete()
    await ctx.send(f"{ctx.author.mention} your suggestion has been sent! Other users can now see your suggestion, if you would like your suggestion removed please contact a High Rank.")
    msg = await channel.send(embed =embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❎")"""
 

@bot.command()
async def hub(ctx):
    """|| gives you link to the Hub!"""
    await ctx.send("https://www.roblox.com/games/6153453289/AV-Hub")

#link to group

@bot.command()
async def group(ctx):
    """|| Gives you link the the group!"""
    await ctx.send("https://www.roblox.com/groups/8644129/AV-Avenir#!/about")

@tasks.loop(seconds = 60)
async def on_member_join(member):
    name1 = (f"Member Count : {member.guild.member_count}")
    chan = member.guild.get_channel(788475887380856913)
    await chan.edit(name=name1)

@bot.command()
async def mb(ctx):
    await ctx.send(f"There are {ctx.guild.member_count} members in the server!")

bot.load_extension("COgs.help")
bot.load_extension("COgs.sell")
bot.load_extension("COgs.moderaion")
bot.load_extension("COgs.apply")
bot.load_extension("COgs.feedback")
bot.load_extension("COgs.logstaff")
bot.run(os.getenv("DISCORDTOKEN"))
