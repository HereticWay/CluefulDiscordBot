import hikari
import lightbulb


class CluefulBot(lightbulb.BotApp):
    def __init__(self, token, guild_id):
        lightbulb.BotApp.__init__(
            self,
            token=token,
            prefix="$",
            banner=None,
            intents=hikari.Intents.ALL, default_enabled_guilds=(guild_id,)
        )
        self.load_extensions_from("./cluefulbot/core/extensions", must_exist=True)
