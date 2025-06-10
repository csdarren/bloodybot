from __future__ import annotations

from typing import TYPE_CHECKING

from msgspec import Struct

if TYPE_CHECKING:
    from datetime import datetime


class BotGuild(Struct, frozen=True, kw_only=True):
    """
    Represents a specified guild of a server

    Attributes
    ----------
    id :class:`int`
        Guild the bot is in
    name :class:`str`
        Guild name where the bot exists
    """
    id: int
    name: str

class BotGuildCategories(Struct, frozen=True, kw_only=True):
    """
    Represents all of the categories of a guild

    Attributes
    ----------
    category_ids :class:`list[int]`
        Category IDs inside of specified guild
    category_names :class:`list[str]`
        Category names inside of specified guild
    """
    category_ids: list[int]
    category_names: list[str]

class BotGuildVoiceChannels(Struct, frozen=True, kw_only=True):
    """
    Represents all of the channels of a guild

    Attributes
    ----------
    voice_channel_ids :class:`list[int]`
        Voice Channel IDs inside of specified guild
    voice_channel_names :class:`list[str]`
        Voice Channel names inside of a specified guild
    """
    voice_channel_ids: list[int]
    voice_channel_names: list[str]

class BotGuildTextChannels(Struct, frozen=True, kw_only=True):
    """
    Represents all of the channels of a guild

    Attributes
    ----------
    text_channel_ids :class:`list[int]`
        Text Channel IDs inside of specified guild
    text_channel_names :class:`list[str]`
        Text Channel names inside of a specified guild
    """
    text_channel_ids: list[int]
    text_channel_names: list[str]

class BotGuildMembers(Struct, frozen=True, kw_only=True):
    """
    Represents all of the members of a guild

    Attributes
    ----------
    member_ids :class:`list[int]`
        Member IDs inside of specified guild
    member_names :class:`list[str]`
        Member Names inside of speficied guild
    """
    member_ids: list[int]
    member_names: list[str]




class CustomChannel(Struct, frozen=True, kw_only=True):
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

class CustomChannelParticipant(Struct, frozen=True, kw_only=True):
    """
    Represents the participants of a Create Channel voice channel

    Attributes
    ----------
    channel: :class:`int`
        channel_id of the created channel
    member: :class:`int`
        member_id of the user that joined
    """
    channel: int
    member: int










class ServerComponents(Struct, frozen=True, kw_only=True):
    """
    """
    guild: int
    categories: int

