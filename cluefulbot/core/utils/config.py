import os


class ConfigParseException(Exception):
    def __init__(self, cause: str):
        super(cause)


def get_token() -> str:
    token = os.getenv("TOKEN")
    if not token:
        raise ConfigParseException("Error: env variable TOKEN is not set!")

    return token


def get_guild_id() -> int:
    guild_id_str = os.getenv("GUILD_ID")
    if not guild_id_str:
        raise ConfigParseException("Error: env variable GUILD_ID is not set!")

    try:
        return int(guild_id_str)
    except ValueError:
        raise ConfigParseException("Error: env variable GUILD_ID is not set!")


def get_lavalink_host() -> str:
    host = os.getenv("LAVALINK_HOST")
    if not host:
        raise ConfigParseException("Error: env variable LAVALINK_HOST is not set!")

    return host


def get_lavalink_password() -> str:
    password = os.getenv("LAVALINK_PASSWORD")
    if not password:
        raise ConfigParseException("Error: env variable LAVALINK_PASSWORD is not set!")

    return password
