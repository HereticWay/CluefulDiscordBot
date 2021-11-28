#!/usr/bin/python3
from bot import bot
import os


def main():
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()


if __name__ == "__main__":
    main()
