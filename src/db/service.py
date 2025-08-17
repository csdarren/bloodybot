from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import asyncpg

from config import dbconf

from . import querys

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from datetime import datetime

    from ..typedefs import BotGuildCustomChannel, BotGuildCustomChannelMember


log = logging.getLogger(__name__)


@asynccontextmanager
async def create_service() -> AsyncGenerator[DbService]:
    async with asyncpg.create_pool(
        user=dbconf.DB_USER,
        password=dbconf.DB_PASS,
        database=dbconf.DB_NAME,
        host=dbconf.DB_HOST,
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

    async def insert_channel(self, dto: BotGuildCustomChannel) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.INSERT_CUSTOM_CHANNEL,
                dto.channel_id,
                dto.guild_id,
                dto.creator_member_id,
                dto.create_ts,
            )
    async def insert_channel_member(self, dto: BotGuildCustomChannelMember) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.INSERT_CUSTOM_CHANNEL_MEMBER,
                dto.channel_id,
                dto.member_id,
            )


    async def select_channel_is_active(self) -> list[int] | None:
        async with self._pool.acquire() as conn, conn.transaction():
            rows = await conn.fetch(
                querys.SELECT_CHANNEL_IS_ACTIVE,
            )
            if rows is None:
                log.info("Failed to retrieve rows, rows = None")
                return None

            return [row["channel_id"] for row in rows]


    async def select_channel_creator_member_id(self, channel_id: int) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            row = await conn.fetchrow(
                querys.SELECT_CHANNEL_CREATOR_MEMBER_ID,
                channel_id
            )
            return row["creator_member_id"]


    async def update_channel_active(self, is_active: bool, delete_time: datetime, channel_id: int) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querys.UPDATE_CHANNEL_IS_ACTIVE,
                is_active,
                delete_time,
                channel_id,
            )

