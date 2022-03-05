#!/usr/bin/python3
from cluefulbot.core import cluefulbot
import os


def main() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    my_bot = cluefulbot.CluefulBot()
    my_bot.run()


if __name__ == "__main__":
    main()
