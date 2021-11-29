from abc import ABC

import hikari
import lightbulb


class Bot(lightbulb.BotApp, ABC):
    def __init__(self, token, guild_id):
        lightbulb.BotApp.__init__(
            self,
            token=token,
            prefix="$",
            banner=None,
            intents=hikari.Intents.ALL, default_enabled_guilds=(guild_id,)
        )
