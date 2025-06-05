from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import asyncpg
from dotenv import load_dotenv

from . import querylist

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from datetime import datetime

    from typedefs import CustomChannelCreate

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

    async def custom_channel_insert(self, dto: CustomChannelCreate) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querylist.CUSTOM_CHANNEL_ENTRY_START,
                dto.channel, # channel ID of channel
                dto.member, # member ID of the user that made channel
                dto.guild, # guild ID that the voice channel was created in
                dto.create_time, # Time the channel was created
            )


    async def get_active_channels(self) -> list[int]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(querylist.SELECT_CHANNEL_ISACTIVE)
        return [row["channel_id"] for row in rows]


    async def get_active_channel_creator(self, channel_id: int) -> int:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                querylist.SELECT_CHANNEL_MEMBER_ISACTIVE,
                channel_id,
            )
            if row is None:
                return 0
            return row["member_id"]


    async def update_channel_active(self, channel_id: int, is_active: bool, delete_time: datetime) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querylist.UPDATE_CHANNEL_ISACTIVE,
                is_active,
                delete_time,
                channel_id,
            )
