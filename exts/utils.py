from discord.ext import commands

from bot import BloodyBot


class UtilitiesCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @commands.command()
    async def reload_ext(self, ctx: commands.Context[BloodyBot]) -> None:
        message = ctx.message.content
        message = message.replace("!reload_ext ", "")
        await ctx.send(f"Reloading extension: {message}")
        await self.bot.reload_extension(f"exts.{message}")

async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(UtilitiesCog(bot))
