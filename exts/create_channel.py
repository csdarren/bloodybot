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
            if not isinstance(channel, VoiceChannel):
                return
            if not channel.members:
                self.created_channel_data.remove([channel, temp_member])
                await channel.delete()


        if after.channel and after.channel.name == "Create Channel":
            target_category = after.channel.category
            if not target_category:
                return
            # Create channel in target_category.
            created_channel = await target_category.create_voice_channel(f"{member.display_name} smelt it recently")
            # Adds the channel to a list that is stored in the bot class for later use in the tasks.
            self.created_channel_data.append([created_channel, member])
            print(f"Moving {member.name} to {created_channel.name}")
            # Moves the member that caused the voice state update to the created channel
            await member.move_to(created_channel)


    @tasks.loop(minutes=30)
    async def update_channel_names(self) -> None:
        for channel, member in self.created_channel_data:
            if not isinstance(channel, VoiceChannel):
                continue
            if channel.name == "Create Channel":
                continue

            creation_time = channel.created_at
            current_time = datetime.now(tz=UTC)
            time_passed = current_time - creation_time
            hours_passed = int(time_passed.total_seconds() / 3600)

            if hours_passed < 1:
                channel_edit_str = f"{member.display_name} smelt it recently"
            else:
                channel_edit_str = f"{member.display_name} smelt it {hours_passed} hours ago"

            if channel.name != channel_edit_str:
                await channel.edit(name=channel_edit_str)


async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CreateChannelCog(bot))
