from __future__ import annotations

from typing import TYPE_CHECKING

from msgspec import Struct

if TYPE_CHECKING:
    from datetime import datetime



class CustomChannelCreate(Struct, frozen=True, kw_only=True):
    """
    Represents the channel created via Create Channel voice channel

    Attributes
    ----------
    channel: :class:`int`
        channel_id of the created channel
    member: :class:`int`
        member_id of the user that created the channel
    guild: :class:`int`
        guild_id of the channel that was created
    create_time: :class:`datetime`
        Time that the channel was created
    """
    channel: int
    member: int
    guild: int
    create_time: datetime
