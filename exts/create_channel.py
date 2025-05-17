import discord
from discord import CategoryChannel, Member, VoiceChannel, VoiceState
from discord.ext import commands

from bot import BloodyBot


class CreateChannelCog(commands.Cog):
    def __init__(self, bot: BloodyBot):
        self.bot = bot

    #@commands.Cog.listener()
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState) -> None:
        for guild in self.bot.guilds:
            target_category = discord.utils.get(guild.categories, name="Voice Channels")

            if after.channel and not before.channel and after.channel.name == "Create Channel":
                print(f"{member.display_name} joined the target channel {after.channel.name}")
                if target_category:
                    created_channel = await guild.create_voice_channel(name=f"{member.name} smelt it", category=target_category)
                    await member.move_to(created_channel)

            if before.channel and not after.channel:
                print(f"{member.name} left the target channel {before.channel.name}")

            for channel in guild.channels:
                if not isinstance(channel, CategoryChannel):
                    if channel.name != "Create Channel" and len(channel.members) == 0:
                        if isinstance(channel, VoiceChannel):
                            await channel.delete()

async def setup(bot: BloodyBot) -> None:
    await bot.add_cog(CreateChannelCog(bot))
