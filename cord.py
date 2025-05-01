from imports import *
from weather import *

intents = cord.Intents.all()

cordo = commands.Bot(command_prefix='!', intents=intents)

@cordo.event
async def on_ready():
	print(f'Logged in as {cordo.user.name}')

@cordo.command()
async def hello(ctx):
	await ctx.send('Hello!')
@cordo.command()
async def weather(ctx):
	await ctx.send(build_weather_report())

cordo.run(os.getenv("CORD_TOKEN"))