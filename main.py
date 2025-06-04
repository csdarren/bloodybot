import asyncio
import os

from dotenv import load_dotenv

from bot import BloodyBot

load_dotenv()

TOKEN = os.environ["CORD_TOKEN"]

async def run_bot() -> None:
    async with (
        BloodyBot() as bot,
    ):
        await bot.start(TOKEN)

def main() -> None:
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
