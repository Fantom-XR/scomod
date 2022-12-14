from datetime import datetime 

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command


class logstaff(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_user_update(self, before, after):
		if before.name != after.name:
			embed = Embed(title="Username change",timestamp=datetime.utcnow())

			fields = [("Before", before.name, False),
					  ("After", after.name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			channel = self.bot.get_channel(914521560839237713)
			await channel.send(embed=embed)

		if before.discriminator != after.discriminator:
			embed = Embed(title="Discriminator change", timestamp=datetime.utcnow())

			fields = [("Before", before.discriminator, False),
					  ("After", after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			
			channel = self.bot.get_channel(914521560839237713)
			await channel.send(embed=embed)

		if before.avatar_url != after.avatar_url:
			embed = Embed(title="Avatar change", description=f" {after.display_name} has changed there Avatar. \n New image is below, old to the right. If the old one does not show this is due to a discord bug which I can not work around.", timestamp=datetime.utcnow())

			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)

			channel = self.bot.get_channel(914521560839237713)
			await channel.send(embed=embed)

	@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed = Embed(title="Nickname change", timestamp=datetime.utcnow())

			fields = [("Before", before.display_name, False),
					  ("After", after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			
			channel = self.bot.get_channel(914521560839237713)
			await channel.send(embed=embed)

		elif before.roles != after.roles:
			embed = Embed(title="Role updates", timestamp=datetime.utcnow())

			fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
					  ("After", ", ".join([r.mention for r in after.roles]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			channel = self.bot.get_channel(914521560839237713)
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

				channel = self.bot.get_channel(914521560839237713)
				await channel.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:
			embed = Embed(title="Message deletion",
						  description=f"Action by {message.author.display_name}.", timestamp=datetime.utcnow())

			fields = [("Content", message.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			channel = self.bot.get_channel(914521560839237713)
			await channel.send(embed=embed)


def setup(bot):
	bot.add_cog(logstaff(bot))
