
from datetime import UTC, datetime

from discord import Member, VoiceChannel, VoiceState
from discord.ext import commands, tasks

from bot import BloodyBot


class CreateChannelCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot
        self.created_channel_data = []
        self.update_channel_names.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        print(f"member: {member.display_name} joined {after.channel} from {before.channel}")

        for channel, temp_member in self.created_channel_data:
            if isinstance(channel, VoiceChannel) and not channel.members:
                self.created_channel_data.remove([channel, temp_member])
                await channel.delete()

        if after.channel and after.channel.name == "Create Channel":
            target_category = after.channel.category
            if target_category:
                # Create channel in target_category.
                created_channel = await target_category.create_voice_channel(f"{member.display_name} smelt it")
                # Adds the channel to a list that is stored in the bot class for later use in the tasks.
                self.created_channel_data.append([created_channel, member])
                print(f"Moving {member.name} to {created_channel.name}")
                # Moves the member that caused the voice state update to the created channel
                await member.move_to(created_channel)

    @tasks.loop(minutes=10)
    async def update_channel_names(self) -> None:
        print("Loop started ----------------------------------------------------------------------------")
        for channel, member in self.created_channel_data:
            if isinstance(channel, VoiceChannel) and channel.name != "Create Channel":
                creation_time = channel.created_at
                current_time = datetime.now(tz=UTC)
                time_passed = current_time - creation_time
                hours_passed = int(time_passed.total_seconds() / 3600)
                if not hours_passed > 1:
                    channel_edit_str = f"{member.display_name} smelt it {hours_passed} hours ago"
                    if channel.name != channel_edit_str:
                        await channel.edit(name=channel_edit_str)
                channel_edit_str = f"{member.display_name} smelt it recently"
                if channel.name != channel_edit_str:
                    await channel.edit(name=channel_edit_str)
        print("Loop ended ------------------------------------------------------------------------------")


async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CreateChannelCog(bot))
