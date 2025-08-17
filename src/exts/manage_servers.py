import asyncio

from discord import ButtonStyle, Interaction, app_commands, ui
from discord.ext import commands

from ..bot import BloodyBot


class ServersMenuView(ui.View):
    def __init__(self):
        super().__init__()
    @ui.button(label="Start MC", style=ButtonStyle.primary)
    async def start_mc(self, i: Interaction, _: ui.Button) -> None:
        cmd = "/srv/mc/runmc.sh"
        try:
            await asyncio.create_subprocess_exec(cmd)
            await i.response.send_message(f"Executing command: {cmd}")
        except Exception as e:
            await i.response.send_message(f"Failed to execute command: {cmd}")
            await i.response.send_message(f"Exception occured: {e}")
    @ui.button(label="Stop MC", style=ButtonStyle.primary)
    async def stop_mc(self, i: Interaction, _: ui.Button) -> None:
        cmd = "/srv/mc/stopmc.sh"
        try:
            await asyncio.create_subprocess_exec(cmd)
            await i.response.send_message(f"Executing command: {cmd}")
        except Exception as e:
            await i.response.send_message(f"Failed to execute command: {cmd}")
            await i.response.send_message(f"Exception occured: {e}")

class StartServers(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @commands.command()
    async def serverview(self, ctx: commands.Context[BloodyBot]) -> None:
        view = ServersMenuView()
        await ctx.send("Server Management", view=view)

    @app_commands.command()
    async def startserver(self, i: Interaction[BloodyBot], server: str) -> None:
        if server == "mc":
            cmd = "/srv/mc/runmc.sh"
            try:
                await asyncio.create_subprocess_exec(cmd)
                await i.response.send_message(f"Executing command: {cmd}")
            except Exception as e:
                await i.response.send_message(f"Failed to execute command: {cmd}")
                await i.response.send_message(f"Exception occured: {e}")
        else:
            # TODO: add other?
            await i.response.send_message("Other?")

    @app_commands.command()
    async def stopserver(self, i: Interaction[BloodyBot], server: str) -> None:
        if server == "mc":
            cmd = "/srv/mc/stopmc.sh"
            try:
                await asyncio.create_subprocess_exec(cmd)
                await i.response.send_message(f"Executing command: {cmd}")
            except Exception as e:
                await i.response.send_message(f"Failed to execute command: {cmd}")
                await i.response.send_message(f"Exception occured: {e}")
        else:
            # TODO: add other?
            await i.response.send_message("Other?")

async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(StartServers(bot))
