from __future__ import annotations

from typing import TYPE_CHECKING

from msgspec import Struct

if TYPE_CHECKING:
    from datetime import datetime

class BotGuildCustomChannel(Struct, frozen=True, kw_only=True):
    """
    Represents a Custom VoiceChannel that was created using the "Create Channel" voice channel

    Attributes
    ----------
    channel_id :class:`int`
        ID of the channel that was created
    guild_id :class:`int`
        Guild ID where the channel exists
    creator_member_id :class:`int`
        Member ID of who created the channel
    create_ts :class:`datetime`
        datetime object that holds the timestamp from when the channel was created
    """
    channel_id: int
    guild_id: int
    creator_member_id: int
    create_ts: datetime

class BotGuildCustomChannelMember(Struct, frozen=True, kw_only=True):
    """
    Represents a member of a Custom VoiceChannel

    Attributes
    ----------
    channel_id :class:`int`
        ID of channel that contains a member
    member_id :class:`int`
        ID of a member of the specified channel
    """

    channel_id: int
    member_id: int
