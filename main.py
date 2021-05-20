import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import traceback

load_dotenv()
intents = discord.Intents.all()

# Discord connection information (bot token and channel to listen to)
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('CHANNEL')

bot = commands.Bot(command_prefix="$", intents=intents)

# Dictionary to store private channel information key: (id) value: (channel_id, persistent: bool)
private_channels = {}

@bot.command(name='create_channel', help='Creates a private channel based on arguments below. Limit one private channel per user')
async def create_channel(ctx):
	user_id = ctx.author.id

	if not ctx.author.voice:
		await ctx.send('You must be in a voice channel to create a private channel.')
		return

	user_channel = ctx.author.voice.channel

	members = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)}

	members[bot.user] = discord.PermissionOverwrite(read_messages=True)

	for m in list(user_channel.voice_states):
		members[await ctx.guild.fetch_member(m)] = discord.PermissionOverwrite(read_messages=True)

	if user_id not in private_channels:
		channel = await ctx.guild.create_text_channel(f'{ctx.author.name}\'s Private Channel', overwrites=members)
		private_channels[user_id] = channel
	else:
		await ctx.send('You already have a private channel.')
		return
	
	await ctx.send(f'Private channel created for {ctx.author.name}. It will delete itself when you leave!')

@bot.command(name='delete_channel', help='Deletes a user channel, if it exists')
async def delete_channel(ctx):
	user_id = ctx.author.id

	if user_id in private_channels:
		channel = private_channels.pop(user_id)
		try:
			await channel.delete()
			await ctx.send('Channel deleted.')
		except Exception:
			return
	else:
		await ctx.send('No private channel to delete.')
		return


@bot.command(name='update_channel', help='Updates the channel with the current members')
async def update_channel(ctx):
	user_id = ctx.author.id

	if not ctx.author.voice:
		await ctx.send('You must be in a voice channel to update a private channel.')
		return

	user_channel = ctx.author.voice.channel

	if user_id in private_channels:
		channel = private_channels[user_id]

		users_added = []

		for m in list(user_channel.voice_states):
			member = await ctx.guild.fetch_member(m)
			await channel.set_permissions(member, read_messages=True)
			users_added.append(member.name)
		
		await ctx.send(f'The following users were added: {users_added}')

	else:
		await ctx.send('No private channel to delete.')
		return


@bot.event
async def on_voice_state_update(member, before, after):
	if member:
		if (before.channel != after.channel) and before.channel:
			# this is a disconnect or a channel switch
			if member.id in private_channels:
				channel = private_channels.pop(member.id)
				try:
					await channel.delete()
				except Exception:
					return


bot.run(TOKEN)