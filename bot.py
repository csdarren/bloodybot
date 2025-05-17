import discord
from discord.ext import commands


class BloodyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
        )
    async def setup_hook(self) -> None:
        try:
            await self.load_extension("exts.create_channel")
        except Exception as e:
            print(f"Failed to load cog: {e}")
        print(f"Logged in as {self.user}")
        print(f"Cog loaded: {self.get_cog("CreateChannelCog")}")


# @WaffleBot.command()
# async def hello(ctx):
#     await ctx.send("Hello!")
# @WaffleBot.command()
# async def weather(ctx):
# 	await ctx.send(build_weather_report())
#
#
# @WaffleBot.command()
# async def join(ctx):
#     for guild in WaffleBot.guilds:
#         member = ctx.author
#         if member.voice:
#             channel = member.voice.channel
#             voice_channel = await channel.connect()
#
#             # Make sure the WaffleBot plays the audio after connecting
#             audio_source = FFmpegPCMAudio("./audio/fart.mp3")  # Ensure the path is correct
#             voice_channel.play(audio_source, after=lambda e: print("Audio finished playing!"))
#
#             await ctx.send(f"Joined {member.name}'s voice channel and started playing audio.")
#         else:
#             await ctx.send(f"{member.name} is not in a voice channel")
#
