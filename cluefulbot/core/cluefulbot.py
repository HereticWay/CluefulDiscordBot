import hikari
import lightbulb
from lightbulb.ext import tasks
from cluefulbot.core.utils.config import *


class CluefulBot(lightbulb.BotApp):
    def __init__(self) -> None:
        lightbulb.BotApp.__init__(
            self,
            token=get_token(),
            prefix="$",
            banner=None,
            intents=hikari.Intents.ALL, default_enabled_guilds=(get_guild_id(),)
        )
        tasks.load(self)

        self.load_extensions_from("./cluefulbot/core/extensions", recursive=True, must_exist=True)
