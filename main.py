import asyncio

from config import botconf
from src.bot import BloodyBot
from src.db.service import create_service


async def run_bot() -> None:
    async with (
        create_service() as dbs,
        BloodyBot(
            dbs=dbs,
        ) as bot,
    ):
        await bot.start(botconf.TOKEN)

def main() -> None:
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
