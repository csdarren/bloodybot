import logging

import discord
from discord import Message
from discord.ext import commands

from .db.service import DbService

TEST_SERVER_ID = "1373809621373943811"
REAL_SERVER_ID = "1114553445035298938"

def setup_logger() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

async def get_prefix(_: commands.Bot, message: Message) -> str:
    if message.guild  and message.guild.id == TEST_SERVER_ID:
        return "@"
    return "!"

logging.basicConfig(level=logging.DEBUG)

class BloodyBot(commands.Bot):
    def __init__(self, dbs: DbService):
        super().__init__( # this super() function setups up commands.Bot, which was passed into the bot.
            command_prefix=get_prefix,
            intents=discord.Intents.all(),
            tree_cls = discord.app_commands.CommandTree
        )
        self.dbs = dbs


    async def setup_hook(self) -> None:
        extensions = ["src.exts.custom_channel",
                      "src.exts.utils",
                      "src.exts.sync",
                      "src.exts.system_services",
                      "src.exts.manage_servers",
                      ]
        for extension in extensions:
            await self.load_extension(extension)
