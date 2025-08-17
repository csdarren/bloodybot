from discord.ext import commands

from ..bot import BloodyBot

GREEN_CHECKMARK = "\U00002705"


class SyncCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: commands.Context[BloodyBot]) -> None:
        await self.bot.tree.sync()

        await ctx.message.add_reaction(GREEN_CHECKMARK)

    @commands.command()
    async def cleartree(self, ctx: commands.Context[BloodyBot]) -> None:
        g = ctx.guild
        if g is None:
            return
        self.bot.tree.clear_commands(guild=g)
        await self.bot.tree.sync(guild=g)
        await ctx.message.add_reaction(GREEN_CHECKMARK)


async def setup(bot: BloodyBot) -> None:
    await bot.tree.sync()
    await bot.add_cog(SyncCog(bot))
