import discord
import os
import random
import requests
import keep_alive
from keep_alive import keep_alive
from discord.ext import commands
from dislash import InteractionClient, Option, OptionType, OptionChoice

bot = commands.Bot(command_prefix = "!")
keep_alive.user = "{0.user}".format(bot)
hello_answers = ["Hello! :)", "Hi!", "What's up?", "Yo!"]
client = InteractionClient(bot, test_guilds = [973967551904223232, 979061394869715005, 979089805080137788])

# import cogs (groups of commands)
from fun import Fun
bot.add_cog(Fun(bot))

@client.event
async def on_message(message):
	if message.author == bot.user: return
	if not bot.user.mentioned_in(message): return
	
	if ("hello" in message.content.lower() or
		"hi" in message.content.lower() or
		"yo" in message.content.lower()):
		await message.reply(random.choice(hello_answers))
	if ("you're cool" in message.content.lower() or
		"smart" in message.content.lower()):
		await message.reply('Thanks! I appreciate the feedback')

@client.slash_command(
	description = "Does Math Sums",
	options = [
		Option("calculation", "Math calculation", OptionType.STRING, True),
		Option("secret", "Only sent to you", OptionType.BOOLEAN, False)
	]
)
async def math(ctx, calculation = "1+1", secret = False):
	embed = discord.Embed()
	embed.colour = discord.Color.orange()
	embed.add_field(name = (eval(calculation)), value = f'is the answer to {calculation}', inline = False)
	try: await ctx.send(embed = embed, ephemeral = secret)
	except (SyntaxError, NameError):
		await ctx.send("There was an error in your requested calculation. Please make sure you have used a valid mathematical expression and that multiplication is signified with an asterix (*).", ephemeral = True)

@client.slash_command(description = 'Invite To your Server!')
async def invite(ctx):
	embed = discord.Embed()
	embed.colour = discord.Colour.orange()
	embed.add_field(name = "Invite to Server", value = "[Invite Here](https://discord.com/api/oauth2/authorize?client_id=973939317900734555&permissions=139586948160&scope=applications.commands%20bot)")
	await ctx.send(embed = embed)
	
@client.slash_command(description = "Shows who helped with the bots' creation!")
async def credits(ctx):
	embed = discord.Embed()
	embed.colour = discord.Color.orange()
	
	embed.add_field(name = '@ninjadev64', value = 'He helped with the coding', inline = False)
	await ctx.send(embed = embed)

weatherkey = os.environ['weatherkey']

@client.slash_command(
	options = [
		Option(
            "option",
			description = "Checks the weather!",
            type = OptionType.STRING,
            required = True,
			choices = [
                OptionChoice("Temperature", "temp"),
                OptionChoice("Cloud Formation", "sky"),
                OptionChoice("Humidity", "humidity"),
				OptionChoice("Wind", "wind")
            ]
        ),
		Option("city", "Choose City", OptionType.STRING, True)
    ]	
)
async def weather(ctx, option: str, city = "London"):
	geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={weatherkey}").json()

	weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={geo[0].get('lat')}&lon={geo[0].get('lon')}&appid=" + weatherkey).json()
	icon = "http://openweathermap.org/img/wn/" + weather.get("weather")[0].get("icon") + "@2x.png"
	
	embed = discord.Embed()
	embed.colour = discord.Colour.orange()
	embed.set_thumbnail(url = icon)
	embed.set_footer(text = f"Weather in {city}")
	
	if option == "temp":
		embed.add_field(name = "Current temperature", value = str(weather.get("main").get("temp")) + "°C")
	elif option == "sky":
		embed.add_field(name = "Sky", value = str(weather.get("weather")[0].get("description")))
	elif option == "humidity":
		embed.add_field(name = "Humidity", value = str(weather.get("main").get("humidity")) + "%")
	elif option == "wind":
		embed.add_field(name = "Wind Speed", value = str(weather.get("wind").get("speed")))
	else:
		embed.add_field(name = "Sorry, there is no such command")
		
	await ctx.send(embed = embed)

@bot.event
async def on_ready():
	print("I am now running in your server as {0.user}! :)".format(bot))

@client.slash_command(description = "Gives a list of all the commands")
async def help(ctx):
	embed = discord.Embed()
	embed.colour = discord.Color.orange()

	embed.add_field(name = "/rickroll", value = "Sends a rickroll link", inline = False)
	embed.add_field(name = "/invite", value = "Invite OwenTheBot to your server!")
	embed.add_field(name = "/math", value = "Does a math sum! To divide, use /, to multiply, use *, to add use +, to take away, use -", inline = False)
	embed.add_field(name = "/spam", value = "Owen the bot will Spam!", inline = False)
	embed.add_field(name = "/weather", value = "Checks the weather in hammersmith!", inline = False)
	embed.add_field(name = "/help", value = "Gets a list of commands", inline = False)
	embed.add_field(name = "/credits", value = "Show who helped with the bot", inline = False)
	embed.add_field(name = "/emojisearch", value = "play a find the input game!", inline = False)
	embed.add_field(name = "/catfact", value = "gets a fact about a cat", inline = False)
	embed.add_field(name = "/secretmath", value = "does a math sum secretly", inline = False)
	embed.add_field(name = "/meme", value = "shows a funny meme", inline = False)
	await ctx.send(embed = embed)

keep_alive()
try: bot.run(os.environ["token"]) 
except discord.errors.HTTPException: os.system("kill 1")