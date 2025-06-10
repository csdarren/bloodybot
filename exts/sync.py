from discord import ChannelType
from discord.ext import commands

from bot import BloodyBot
from typedefs import BotGuild, BotGuildCategories, BotGuildMembers, BotGuildTextChannels, BotGuildVoiceChannels

GREEN_CHECKMARK = "\U00002705"


class SyncCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx: commands.Context[BloodyBot]) -> None:
        await self.bot.tree.sync()
        await ctx.message.add_reaction(GREEN_CHECKMARK)

    @commands.command()
    async def sync_server(self, ctx: commands.Context[BloodyBot]) -> None:
        g = ctx.guild
        if g is None:
            return

        all_channels = await g.fetch_channels()
        all_members = []
        async for member in g.fetch_members():
            all_members.append(member)

        category_ids = []
        category_names = []

        member_ids = []
        member_names = []

        voice_channel_ids = []
        voice_channel_names = []

        text_channel_ids = []
        text_channel_names = []

        for channel in all_channels:
            if channel.type == ChannelType.category:
                category_ids.append(channel.id)
                category_names.append(channel.name)

            elif channel.type == ChannelType.voice:
                voice_channel_ids.append(channel.id)
                voice_channel_names.append(channel.name)

            elif channel.type == ChannelType.text:
                text_channel_ids.append(channel.id)
                text_channel_names.append(channel.name)

            else:
                await ctx.send(f"""Channels that slipped past:
                {channel.name}
                {channel.id}
                {channel.type}
                        """)

        for member in all_members:
            member_ids.append(member.id)
            member_names.append(member.name)


        dto1 = BotGuild(id=g.id, name=g.name)
        dto2 = BotGuildCategories(category_ids=category_ids, category_names=category_names)
        dto3 = BotGuildMembers(member_ids=member_ids, member_names=member_names)
        dto4 = BotGuildVoiceChannels(voice_channel_ids=voice_channel_ids, voice_channel_names=voice_channel_names)
        dto5 = BotGuildTextChannels(text_channel_ids=text_channel_ids, text_channel_names=text_channel_names)

        await self.bot.dbs.sync_guild(g.id, dto1)
        await self.bot.dbs.sync_categories(g.id, dto2)
        await self.bot.dbs.sync_members(g.id, dto3)
        await self.bot.dbs.sync_voice_channels(g.id, dto4)
        await self.bot.dbs.sync_text_channels(g.id, dto5)


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
