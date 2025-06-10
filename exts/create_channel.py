from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord import Interaction, Member, VoiceState

    from bot import BloodyBot
from datetime import UTC, datetime

from discord import TextChannel, VoiceChannel, app_commands
from discord.ext import commands, tasks

from typedefs import CustomChannel, CustomChannelParticipant

TEST_GUILD_ID = 1373809621373943811
REAL_GUILD_ID = 1114553445035298938


async def get_active_channels_obj(bot: BloodyBot) -> list[VoiceChannel] | None:
    channels: list[VoiceChannel] = []
    active_channels = await bot.dbs.get_active_channels()
    for channel_id in active_channels:
        channel = bot.get_channel(channel_id)
        # check to see if they are cached by bot first to avoid pointless processing
        if channel is None:
            channel = await bot.fetch_channel(channel_id)
        if not isinstance(channel, VoiceChannel):
            return None
        channels.append(channel)
    return channels


class CreateChannelCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot
        self.update_channel_names.start()
        self.test_guild = self.bot.get_guild(TEST_GUILD_ID)
        self.real_guild = self.bot.get_guild(REAL_GUILD_ID)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, _before: VoiceState, after: VoiceState) -> None:
        # TODO: log this: print(f"member: {member.display_name} joined {after.channel} from {before.channel}")
        _ = _before


        # get list of channel id's that are active, convert to channel objects and iterate through them
        active_channels = await self.bot.dbs.get_active_channels()
        for channel_id in active_channels:
            if after.channel and after.channel.id == channel_id:
                dto = CustomChannelParticipant(
                    channel=after.channel.id,
                    member=member.id
                )
                await self.bot.dbs.custom_channel_participant_insert(dto=dto)


            channel = self.bot.get_channel(channel_id)
            # check to see if they are cached by bot first to avoid pointless processing
            if channel is None:
                channel = await self.bot.fetch_channel(channel_id)
            if not isinstance(channel, VoiceChannel):
                return
            if not channel.members:
                await channel.delete()
                await self.bot.dbs.update_channel_active(channel.id, False, datetime.now(UTC))
                # set channel to inactive in database after deleting


        if after.channel and after.channel.name == "Create Channel":
            target_category = after.channel.category
            if not target_category:
                return
            # Create channel in target_category.
            created_channel = await target_category.create_voice_channel(f"{member.display_name} smelt it recently")
            # define dto that is used to insert to database
            # TODO: log this: print(f"guild ID: {created_channel.guild.id}")
            dto = CustomChannel(
                channel=created_channel.id,
                guild=created_channel.guild.id,
                member=member.id,
                create_time=created_channel.created_at,
            )
            # inserts dto into database

            await self.bot.dbs.custom_channel_insert(dto=dto)
            if after.channel.id == created_channel.id:
                dto = CustomChannelParticipant(
                    channel=created_channel.id,
                    member=member.id
                )
                await self.bot.dbs.custom_channel_participant_insert(dto=dto)


            # TODO: log this: print(f"Moving {member.name} to {created_channel.name}")
            # Moves the member that caused the voice state update to the created channel
            await member.move_to(created_channel)



    @tasks.loop(minutes=30)
    async def update_channel_names(self) -> None:
        active_channels = await get_active_channels_obj(self.bot)
        if not active_channels:
            return
        for channel in active_channels:
            creation_time = channel.created_at
            current_time = datetime.now(tz=UTC)
            time_passed = current_time - creation_time
            hours_passed = int(time_passed.total_seconds() / 3600)

            channel_guild = channel.guild
            channel_creator_id = await self.bot.dbs.get_active_channel_creator(channel.id)
            member = channel_guild.get_member(channel_creator_id)
            if not member:
                member = await channel_guild.fetch_member(channel_creator_id)
                # TODO: Add a real check here for when member is not accurately grabbed from db

            if hours_passed < 1:
                channel_edit_str = f"{member.display_name} smelt it recently"
            else:
                channel_edit_str = f"{member.display_name} smelt it {hours_passed} hours ago"

            if channel.name != channel_edit_str:
                await channel.edit(name=channel_edit_str)

    @app_commands.command()
    async def retrieve_channel_details(self, i: Interaction, date: str) -> None:
        date += "+0000" # Add timezone info for UTC
        datetime_obj = datetime.strptime(date, "%m-%d-%Y%z")
        channel_ids = await self.bot.dbs.get_created_channels_timestamp(datetime_obj)
        channel_members = []
        for channel_id in channel_ids:
            channel_member_ids = await self.bot.dbs.get_created_channels_members(channel_id)
            if self.real_guild is None:
                continue
            for channel_member_id in channel_member_ids:
                member = self.real_guild.get_member(channel_member_id)
                if member is None:
                    continue
                channel_members.append(member.display_name)

            current_channel = i.channel
            if isinstance(current_channel, TextChannel):
                await current_channel.send(f"""
                channel: {channel_id}

                members: {channel_members}
                                            """)


async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CreateChannelCog(bot))
