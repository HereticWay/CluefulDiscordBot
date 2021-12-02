#!/usr/bin/python3
from cluefulbot.core import cluefulbot
import typing as t
import os
import sys


def parse_settings() -> t.Tuple[str, int]:
    token: str = os.getenv("TOKEN")
    guild_id: str = os.getenv("GUILD_ID")
    if not token or not guild_id:
        print("Please specify both TOKEN and GUILD_ID environment variables!", file=sys.stderr)
        quit(1)

    try:
        guild_id_int = int(guild_id)
    except ValueError:
        print("GUILD_ID environment variable should be an integer!", file=sys.stderr)
        quit(1)

    return token, guild_id_int


def main() -> None:
    if os.name != "nt":
        import uvloop
        uvloop.install()

    token, guild_id = parse_settings()
    my_bot = cluefulbot.CluefulBot(token=token, guild_id=guild_id)
    my_bot.run()


if __name__ == "__main__":
    main()
