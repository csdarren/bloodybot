from datetime import UTC, datetime

from discord import ButtonStyle, Interaction, TextChannel, ui
from discord.ext import commands

from ..bot import BloodyBot

GREEN_CHECKMARK = "\U00002705"

class UtilsView(ui.View):
    def __init__(self, bot: BloodyBot):
        super().__init__()
        self.bot = bot
    @ui.button(label="Reload Custom Channel", style=ButtonStyle.primary)
    async def reload_cc(self, i: Interaction, _: ui.Button) -> None:
        ext = "src.exts.custom_channel"
        await self.bot.reload_extension(ext)
        await i.response.send_message(f"Reloading: {ext}", ephemeral=True)
    @ui.button(label="Reload Admin Utils", style=ButtonStyle.primary)
    async def reload_au(self, i: Interaction, _: ui.Button) -> None:
        ext = "src.exts.utils"
        await self.bot.reload_extension(ext)
        await i.response.send_message(f"Reloading: {ext}", ephemeral=True)

class UtilitiesCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @commands.command()
    async def utilview(self, ctx: commands.Context[BloodyBot]) -> None:
        view = UtilsView(self.bot)
        await ctx.send("Admin Util Menu", view=view)

    @commands.command()
    async def prune(self, ctx: commands.Context[BloodyBot], amt: int) -> None:
        channel = ctx.channel
        if isinstance(channel, TextChannel):
            await channel.purge(limit=amt)

    @commands.command()
    async def get_channel_creation(self, ctx: commands.Context[BloodyBot], channel_id: int) -> None:
        g = ctx.guild
        if g is None:
            return
        channel = g.get_channel(channel_id)
        if channel is None:
            return

        creation_time = channel.created_at
        current_time = datetime.now(tz=UTC)
        time_passed = current_time - creation_time
        minutes_passed = int(time_passed.total_seconds() / 3600)

        await ctx.send(f"Channel {channel.name} was created at: {creation_time}")
        await ctx.send(f"Channel {channel.name} was created {minutes_passed} hours ago")

    @commands.command()
    async def reload_ext(self, ctx: commands.Context[BloodyBot], ext: str) -> None:
        await ctx.send(f"Reloading Extension: {ext}")
        await self.bot.reload_extension(ext)

    @commands.command()
    async def load_ext(self, ctx: commands.Context[BloodyBot], ext: str) -> None:
        await ctx.send(f"Reloading Extension: {ext}")
        await self.bot.load_extension(ext)

    @commands.command()
    async def unload_ext(self, ctx: commands.Context[BloodyBot], ext: str) -> None:
        await ctx.send(f"Reloading Extension: {ext}")
        await self.bot.unload_extension(ext)


async def setup(bot: BloodyBot) -> None:
    await bot.tree.sync()
    await bot.add_cog(UtilitiesCog(bot))
