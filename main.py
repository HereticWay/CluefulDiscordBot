#!/usr/bin/python3
import bot
import os

GUILD_ID = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv('TOKEN')


def main():
    if os.name != "nt":
        import uvloop
        uvloop.install()

    my_bot = bot.Bot(token=TOKEN, guild_id=GUILD_ID)
    my_bot.load_extensions_from("./extensions/", must_exist=True)
    my_bot.run()


if __name__ == "__main__":
    main()
