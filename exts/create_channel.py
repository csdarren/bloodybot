
from datetime import UTC, datetime

from discord import Member, VoiceChannel, VoiceState
from discord.ext import commands, tasks

from bot import BloodyBot


class CreateChannelCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot
        self.created_channels_id: set[int] = set()
        self.members_created_channels: set [Member] = set()
        self.update_channel_names.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        print(f"member: {member.display_name} joined {after.channel} from {before.channel}")

        for channel_id in self.created_channels_id:
            channel = self.bot.get_channel(channel_id)
            if isinstance(channel, VoiceChannel) and not channel.members:
                await channel.delete()

        if after.channel and after.channel.name == "Create Channel":
            target_category = after.channel.category
            if target_category:
                # Create channel in target_category.
                created_channel = await target_category.create_voice_channel(f"{member.display_name} smelt it")
                # Adds the created channels ID to a set of channel ids that is stored in self.created_channels_id
                self.created_channels_id.add(created_channel.id)
                self.members_created_channels.add(member)
                print(f"Moving {member.name} to {created_channel.name}")
                # Moves the member that caused the voice state update to the created channel
                await member.move_to(created_channel)

    @tasks.loop(minutes=1)
    async def update_channel_names(self) -> None:
        print("Loop started ----------------------------------------------------------------------------")
        for channel_id in self.created_channels_id:
            for member in self.members_created_channels:
                channel = self.bot.get_channel(channel_id)
                if isinstance(channel, VoiceChannel) and channel.name != "Create Channel":
                    creation_time = channel.created_at
                    current_time = datetime.now(tz=UTC)
                    time_passed = current_time - creation_time
                    hours_passed = int(time_passed.total_seconds() / 3600)
                    await channel.edit(name=f"{member.display_name} smelt it {hours_passed} hours ago")
        print("Loop ended ------------------------------------------------------------------------------")



async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CreateChannelCog(bot))
