from datetime import datetime 

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from better_profanity import profanity


profanity.load_censor_words_from_file("./data/profanity.txt")


class auto(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
          if not message.author.bot:
            if profanity.contains_profanity(message.content):
              await message.delete()
              await message.channel.send(f"{message.author.mention}, you can't use that word here! {message.content}")
              await message.author.send(f"Original Message sent in {message.guild}: ```{message.content}```")


	"""@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed = Embed(title="Nickname change", timestamp=datetime.utcnow())

			fields = [("Before", before.display_name, False),
					  ("After", after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			
			channel = self.bot.get_channel(881640389126271006)
			await channel.send(embed=embed)

		elif before.roles != after.roles:
			embed = Embed(title="Role updates", timestamp=datetime.utcnow())

			fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
					  ("After", ", ".join([r.mention for r in after.roles]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			channel = self.bot.get_channel(881640389126271006)
			await channel.send(embed=embed)

	@Cog.listener()
	async def on_message_edit(self, before, after):
		if not after.author.bot:
			if before.content != after.content:
				embed = Embed(title="Message edit",
							  description=f"Edit by {after.author.display_name}.", timestamp=datetime.utcnow())

				fields = [("Before", before.content, False),
						  ("After", after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				channel = self.bot.get_channel(881640389126271006)
				await channel.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:
			embed = Embed(title="Message deletion",
						  description=f"Action by {message.author.display_name}.", timestamp=datetime.utcnow())

			fields = [("Content", message.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			channel = self.bot.get_channel(881640389126271006)
			await channel.send(embed=embed)"""


def setup(bot):
	bot.add_cog(auto(bot))
