import asyncio

from discord import Interaction, app_commands
from discord.ext import commands

from ..bot import BloodyBot


class SystemServices(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @app_commands.command()
    async def manage_service(self, i: Interaction[BloodyBot], action: str, process: str) -> None:
        await i.response.send_message(f"Executing Command: {action}, on process: {process}")
        try:
            if i.user.name != "realwafflz":
                await i.response.send_message(f"Failed to execute command: {action}, on process: {process} - Invalid Permissions")
                return

            await asyncio.create_subprocess_exec("/bin/systemctl", action, process)
            await i.response.send_message("Successfully executed command")

        except:
            await i.response.send_message(f"Failed to execute command: {action}, on process: {process}")

async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(SystemServices(bot))
