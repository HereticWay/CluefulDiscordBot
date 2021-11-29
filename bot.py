import os
import hikari
import lightbulb

from lightbulb import commands, context

GUILD_ID = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv('TOKEN')

bot = lightbulb.BotApp(
    token=TOKEN,
    prefix="$",
    banner=None,
    intents=hikari.Intents.ALL, default_enabled_guilds=(GUILD_ID,)
)
bot.load_extensions_from("./extensions/", must_exist=True)
