#!/usr/bin/python3
from cluefulbot.core import cluefulbot
import os

GUILD_ID = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv('TOKEN')


def main():
    if os.name != "nt":
        import uvloop
        uvloop.install()

    my_bot = cluefulbot.CluefulBot(token=TOKEN, guild_id=GUILD_ID)
    my_bot.run()


if __name__ == "__main__":
    main()
