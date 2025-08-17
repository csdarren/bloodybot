from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..typedefs import BotGuildCustomChannel, BotGuildCustomChannelMember

if TYPE_CHECKING:
    from discord import Member, VoiceState

    from ..bot import BloodyBot
from datetime import UTC, datetime

from discord import Member, NotFound, VoiceChannel
from discord.abc import GuildChannel
from discord.ext import commands, tasks

log = logging.getLogger(__name__)


def get_hours_passed(channel_ts: datetime) -> int:
    current_time = datetime.now(tz=UTC)
    time_passed = current_time - channel_ts
    return int(time_passed.total_seconds() / 3600) # convert seconds to hours by dividing by 60 x 60 (3600)

async def get_active_channels(bot: BloodyBot) -> list[VoiceChannel] | None:
    active_channel_ids = await bot.dbs.select_channel_is_active()

    if active_channel_ids is None:
        log.error("active_channel_ids is None")
        return None

    active_channels = []
    for active_channel_id in active_channel_ids:
        active_channel = bot.get_channel(active_channel_id)
        if active_channel is None:
            try:
                active_channel = await bot.fetch_channel(active_channel_id)
            except NotFound:
                log.exception("Channel Not Found")
                return None

        if not isinstance(active_channel, VoiceChannel):
            if isinstance(active_channel, GuildChannel): # TODO: Find a better way to do this without the 2nd if statment
                log.info("active_channel was determined to be not a VoiceChannel? ChannelType: %s", active_channel.type)
            return None

        active_channels.append(active_channel)

    return active_channels

async def get_channel_creator(channel: VoiceChannel, bot: BloodyBot) -> Member | None:
    creator_id = await bot.dbs.select_channel_creator_member_id(channel.id)
    if creator_id is None:
        log.error("Bad creator_id")
        return None
    guild = channel.guild
    creator = guild.get_member(creator_id)
    if creator is None:
        creator = await guild.fetch_member(creator_id)
        if creator is None:
            log.debug("creator was not found using get_member, needed to fetch.")


class CustomChannelCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot
        self.update_channel_names.start()


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        log.info("member: %s joined %s from %s", member.display_name, after.channel, before.channel)

        if after.channel and after.channel.name == "Create Channel":
            target_category = after.channel.category
            if not target_category:
                log.error("target_category broken")
                return
            # Create channel in target_category.
            created_channel = await target_category.create_voice_channel(f"{member.display_name} smelt it recently")
            log.info("Created %s in %s", target_category, created_channel)

            # define channel dto that is used to insert the channel to the database
            dto = BotGuildCustomChannel(
                channel_id=created_channel.id,
                guild_id=created_channel.guild.id,
                creator_member_id=member.id,
                create_ts=created_channel.created_at,
            )

            # inserts dto into database
            await self.bot.dbs.insert_channel(dto=dto)
            log.info("Inserted %s to the database", created_channel)

            await member.move_to(created_channel)
            log.info("Moved %s to %s", member.display_name, created_channel)

        # defines a dto to insert member to a specific channel in the database. (Keeps track of who joins what channel)
        if after.channel and after.channel.name != "Create Channel":
            member_dto = BotGuildCustomChannelMember(
                channel_id=after.channel.id,
                member_id=member.id,
            )
            await self.bot.dbs.insert_channel_member(member_dto)

        active_channels = await get_active_channels(self.bot)
        if active_channels is None:
            log.error("active_channels is none")
            return
        for active_channel in active_channels:
            if active_channel and not active_channel.members:
                await active_channel.delete()
                await self.bot.dbs.update_channel_active(False, datetime.now(UTC), active_channel.id)
                log.info("Deleted Channel: %s and updating is_active status in DB", active_channel)
            else:
                log.info("active_channel is None, or there are zero empty channels")


    @tasks.loop(minutes=55)
    async def update_channel_names(self) -> None:
        active_channels = await get_active_channels(self.bot)
        if active_channels is None:
            log.error("active_channels is None")
            return
        for active_channel in active_channels:
            creator = await get_channel_creator(active_channel, self.bot)

            if creator is Member: # TODO: Do this without the if statement. I tried if creator is None: return
                hours_passed = get_hours_passed(active_channel.created_at)

                if hours_passed < 1:
                    channel_edit_str = f"{creator.display_name} smelt it recently"

                elif hours_passed == 1:
                    channel_edit_str = f"{creator.display_name} smelt it {hours_passed} hr ago"

                else:
                    channel_edit_str = f"{creator.display_name} smelt it {hours_passed} hrs ago"


                if active_channel.name != channel_edit_str:
                    # check to see if they are cached by bot first to avoid pointless api calls
                    await active_channel.edit(name=channel_edit_str)

async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CustomChannelCog(bot))
