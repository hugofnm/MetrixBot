import os
import io
import datetime
import json
from aiohttp import ClientSession
import ksoftapi
import keep_alive
import discord
from discord.ext import commands
from os import environ, listdir

keep_alive.keep_alive()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("&"),
					description='DrunkCat, a Discord bot created by @hugofnm#8066 with ❤️ in Nice, France. Status : status.hugofnm.fr',
					case_insensitive=True,
					intents=discord.Intents.all())

bot.remove_command('help')

bot.uptime = datetime.datetime.now()
bot.messages_in = bot.messages_out = 0
bot.region = 'Nice, FR'

@bot.event
async def on_ready():
	print('Connecté comme {0} ({0.id})'.format(bot.user))
	bot.kclient = ksoftapi.Client(os.environ['KSoft_Token'])
	bot.client = ClientSession()

	# Load Modules
	modules = ['debug', 'games', 'media', 'misc', 'music']
	try:
		for module in modules:
			bot.load_extension('cogs.' + module)
			print('Loaded: ' + module)
	except Exception as e:
		print(f'Error loading {module}: {e}')

	print('Bot.....Activated')
	await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="eating final bugs"))

@bot.event
async def on_message(message):
	# Sent message
	if message.author.id == bot.user.id:
		if hasattr(bot, 'messages_out'):
			bot.messages_out += 1
	# Received message (Count only commands messages)
	elif message.content.startswith('~'):
		if hasattr(bot, 'messages_in'):
			bot.messages_in += 1

	await bot.process_commands(message)

#Bot event with hello and goodbye messages

#@bot.event
#async def on_member_join(member):
#	sys_channel = member.guild.system_channel
#	if sys_channel:
#		data = await canvas.member_banner('Bonjour', str(member), str(member.avatar_url_as(format='png', size=256)))
#		with io.BytesIO() as img:
#			data.save(img, 'PNG')
#			img.seek(0)
#			try:
#				await sys_channel.send(content=member.mention, file=discord.File(fp=img, filename='welcome.png'))
#			except discord.Forbidden:
#				pass

#@bot.event
#async def on_member_remove(member):
#	sys_channel = member.guild.system_channel
#	if sys_channel:
#		data = await canvas.member_banner('Au revoir', str(member), str(member.avatar_url_as(format='png', size=256)))
#		with io.BytesIO() as img:
#			data.save(img, 'PNG')
#			img.seek(0)
#			try:
#				await sys_channel.send(file=discord.File(fp=img, filename='leave.png'))
#			except discord.Forbidden:
#				pass

#end

@bot.command(name='help', aliases=['h'])
async def help(ctx, arg: str=''):
	"""Montre l'écran d'aide"""
	embed = discord.Embed(title="DrunkCat, a Discord bot created by @hugofnm#8066 with ❤️ in Nice, France. Status : status.hugofnm.fr", colour=discord.Colour(0x7f20a0))

	avatar_url = str(bot.user.avatar_url)
	embed.set_thumbnail(url=avatar_url)
	embed.set_author(name="DrunkCat Bot Help", url="https://discord.com/oauth2/authorize?client_id=735564887056580640&scope=bot&permissions=8", icon_url=avatar_url)
	embed.set_footer(text="Drunk Bot par @hugofnm#8066")

	if arg.strip().lower() == '-a':
		# Full version
		embed.description = 'Mon préfix d\'appel est `&`'
		with open('help.json', 'r') as help_file:
			data = json.load(help_file)
		data = data['full']
		for key in data:
			value = '\n'.join(x for x in data[key])
			embed.add_field(name=key, value=f"```{value}```", inline=False)
	else:
		# Short version
		embed.description = 'Mon préfix d\'appel est `&`, tapez &help -a pour plus d\'informations sur les commandes'
		with open('help.json', 'r') as help_file:
			data = json.load(help_file)
		data = data['short']
		for key in data:
			embed.add_field(name=key, value=data[key])
	try:
		await ctx.send(embed=embed)
	except Exception:
		await ctx.send("Je n'ai pas la permission d'envoyer des embed ici :\'('")


# All good ready to start!
print('Starting Bot...')
bot.run(os.environ['TOKEN'])