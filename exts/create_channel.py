from datetime import UTC, datetime

from discord import Member, VoiceChannel, VoiceState
from discord.ext import commands, tasks

from bot import BloodyBot
from typedefs import CustomChannelCreate


async def list_active_channels(bot: BloodyBot) -> list[VoiceChannel] | None:
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


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        print(f"member: {member.display_name} joined {after.channel} from {before.channel}")


        # get list of channel id's that are active, convert to channel objects and iterate through them
        active_channels = await self.bot.dbs.get_active_channels()
        for channel_id in active_channels:
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
            print(f"guild ID: {created_channel.guild.id}")
            dto = CustomChannelCreate(
                channel=created_channel.id,
                guild=created_channel.guild.id,
                member=member.id,
                create_time=created_channel.created_at,
            )
            # inserts dto into database
            await self.bot.dbs.custom_channel_insert(dto=dto)


            print(f"Moving {member.name} to {created_channel.name}")
            # Moves the member that caused the voice state update to the created channel
            await member.move_to(created_channel)


    @tasks.loop(minutes=30)
    async def update_channel_names(self) -> None:
        active_channels = await list_active_channels(self.bot)
        if not active_channels:
            return
        for channel in active_channels:
            creation_time = channel.created_at
            current_time = datetime.now(tz=UTC)
            time_passed = current_time - creation_time
            hours_passed = int(time_passed.total_seconds() / 3600)

            channel_creator_id = await self.bot.dbs.get_active_channel_creator(channel.id)
            member = channel.guild.get_member(channel_creator_id)
            if not member:
                # TODO: Add a real check here for when member is not accurately grabbed from db
                continue

            if hours_passed < 1:
                channel_edit_str = f"{member.display_name} smelt it recently"
            else:
                channel_edit_str = f"{member.display_name} smelt it {hours_passed} hours ago"

            if channel.name != channel_edit_str:
                await channel.edit(name=channel_edit_str)


async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CreateChannelCog(bot))
