from __future__ import annotations

from typing import TYPE_CHECKING

from msgspec import Struct

if TYPE_CHECKING:
    import discord
    from discord import VoiceChannel

    from bot import BloodyBot

class CustomChannel(Struct, frozen=True, kw_only=True):
    """
    Represents the channel created via Create Channel voice channel

    Attributes
    ----------
    i: :class:`discord.Interaction`
        The Discord interaction associated with the report.
    member: :class:`discord.Member`
        Member object of the user that created the channel
    channel: :class:`discord.VoiceChannel`
        VoiceChannel object of the created channel
    create_time: :class:`str`
        Time that the channel was created
    delete_time: :class:`str`
        Time that the channel was deleted
    hours_active: :class:`int`
        Number of hours the channel was active
    users_present_when_active: :class:`list[str]`
        Full list of users that were present while channel was active
    is_active: :class:`bool`
        Channel active = true. Channel inactive = false.
    notes: :class:`str`
        Any additional notes
    """
    i: discord.Interaction[BloodyBot]
    member: discord.Member
    channel: VoiceChannel
    create_time: str
    delete_time: str
    hours_active: int
    users_present_when_active: list[str]
    is_active: bool
    notes: str

