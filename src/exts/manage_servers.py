import asyncio

from discord import Interaction, app_commands
from discord.ext import commands

from bot import BloodyBot


class StartServers(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @app_commands.command()
    async def startserver(self, i: Interaction[BloodyBot], server: str) -> None:
        if server == "mc":
            cmd = "/srv/bloodybot/runmc.sh"
            try:
                await asyncio.create_subprocess_exec(cmd)
                await i.response.send_message(f"Executing command: {cmd}")
            except Exception as e:
                await i.response.send_message(f"Failed to execute command: {cmd}")
                await i.response.send_message(f"Exception occured: {e}")

    @app_commands.command()
    async def stopserver(self, i: Interaction[BloodyBot], server: str) -> None:
        if server == "mc":
            cmd = "/srv/bloodybot/stopmc.sh"
            try:
                await asyncio.create_subprocess_exec(cmd)
                await i.response.send_message(f"Executing command: {cmd}")
            except Exception as e:
                await i.response.send_message(f"Failed to execute command: {cmd}")
                await i.response.send_message(f"Exception occured: {e}")
        else:
            await i.response.send_message()

async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(StartServers(bot))
