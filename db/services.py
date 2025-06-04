from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import asyncpg

from . import querylist

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from typedefs import CustomChannel


@asynccontextmanager
async def create_service() -> AsyncGenerator[DbService]:
    async with asyncpg.create_pool(
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

    async def insert_custom_channel(self, dto: CustomChannel) -> None:
        async with self._pool.acquire() as conn, conn.transaction():
            await conn.execute(
                querylist.INSERT_CUSTOM_CHANNEL,
                dto.i.user.id,
                dto.i.created_at,
                dto.member.id,
                dto.create_time,
                dto.delete_time,
                dto.hours_active,
                # WIP dto.users_present_when_active,
                dto.is_active,
                dto.notes,
            )
