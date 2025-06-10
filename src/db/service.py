from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import asyncpg
from asyncpg import Record
from dotenv import load_dotenv

from . import querys

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from datetime import datetime

    from typedefs import (
        BotGuild,
        BotGuildCategories,
        BotGuildMembers,
        BotGuildTextChannels,
        BotGuildVoiceChannels,
        CustomChannel,
        CustomChannelParticipant,
    )


load_dotenv()

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]

@asynccontextmanager
async def create_service() -> AsyncGenerator[DbService]:
    async with asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
        min_size=1,  # initiate N connections on startup
        max_size=5,  # hard limit N connections
        server_settings={
            "application_name": "bloodybot",
        },
    ) as pool:
        yield DbService(pool)

class DbService:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    # INSERT

    async def custom_channel_insert(self, dto: CustomChannel) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.INSERT_CUSTOM_CHANNEL,
                dto.channel, # channel ID of channel
                dto.guild, # guild ID that the voice channel was created in
                dto.member, # member ID of the user that made channel
                dto.create_time, # Time the channel was created
            )

    async def custom_channel_participant_insert(self, dto: CustomChannelParticipant) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.INSERT_CUSTOM_CHANNEL_PARTICIPANTS,
                dto.channel,
                dto.member,
            )


    async def sync_guild(self, guild_id: int, dto: BotGuild) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.INSERT_BOT_GUILDS,
                guild_id,
                dto.name,
            )

    async def sync_categories(self, guild_id: int, dto: BotGuildCategories) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            for category_id, category_name in zip(dto.category_ids, dto.category_names, strict=False):
                await conn.execute(
                    querys.INSERT_GUILD_CATEGORY,
                    category_id,
                    category_name,
                    guild_id,
                )

    async def sync_voice_channels(self, guild_id: int, dto: BotGuildVoiceChannels) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            for voice_channel_id, voice_channel_name in zip(dto.voice_channel_ids, dto.voice_channel_names, strict=False):
                await conn.execute(
                    querys.INSERT_GUILD_VOICE_CHANNEL,
                    voice_channel_id,
                    voice_channel_name,
                    guild_id,
                )

    async def sync_text_channels(self, guild_id: int, dto: BotGuildTextChannels) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            for text_channel_id, text_channel_name in zip(dto.text_channel_ids, dto.text_channel_names, strict=False):
                await conn.execute(
                    querys.INSERT_GUILD_TEXT_CHANNEL,
                    text_channel_id,
                    text_channel_name,
                    guild_id,
                )

    async def sync_members(self, guild_id: int, dto: BotGuildMembers) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            for member_id, member_name in zip(dto.member_ids, dto.member_names, strict=False):
                await conn.execute(
                    querys.INSERT_GUILD_MEMBER,
                    member_id,
                    member_name,
                    guild_id,
                )


    # SELECT

    async def get_active_channels(self) -> list[int]:
        async with self._pool.acquire() as conn:
            rows: list[Record] = await conn.fetch(querys.SELECT_CHANNEL_ISACTIVE)
        return [row["channel_id"] for row in rows]


    async def get_active_channel_creator(self, channel_id: int) -> int:
        async with self._pool.acquire() as conn:
            row: Record = await conn.fetchrow(
                querys.SELECT_CHANNEL_MEMBER_ISACTIVE,
                channel_id,
            )
            if row is None:
                return 0
            return row["member_id"]

    async def get_created_channels_timestamp(self, datetime: datetime) -> list[int]:
        async with self._pool.acquire() as conn:
            rows: list[Record] = await conn.fetch(
                querys.SELECT_CHANNELS_TIMESTAMP,
                datetime.date(),
            )
            return [row["channel_id"] for row in rows]

    async def get_created_channels_members(self, channel_id: int) -> list[int]:
        async with self._pool.acquire() as conn:
            rows: list[Record] = await conn.fetch(
                querys.SELECT_CHANNEL_PARTICIPANTS,
                channel_id,
            )
            return [row["member_id"] for row in rows]


    # UPDATE

    async def update_channel_active(self, channel_id: int, is_active: bool, delete_time: datetime) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.UPDATE_CHANNEL_ISACTIVE,
                is_active,
                delete_time,
                channel_id,
            )
