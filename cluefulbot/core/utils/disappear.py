from cluefulbot.core.utils import utils
from lightbulb import context
import hikari
import asyncio
import functools


def disappear(after: int):
    """Decorator to make a command's context disappear after the given number of seconds.

    Args:
        after (int): number of seconds to disappear
    """
    if type(after) is not int:
        raise TypeError("Argument after should be an integer!")
    if after < 1:
        raise ValueError("Argument after should be a positive integer!")

    def decorator(wrapped_function):
        @functools.wraps(wrapped_function)
        async def wrapper(ctx: context.Context):
            await wrapped_function(ctx)
            await asyncio.sleep(after)

            channel: hikari.GuildChannel = ctx.get_channel()
            if utils.is_prefix_command(ctx):
                context_messages = frozenset([await response.message() for response in ctx.responses])
                command_message = ctx.event.message
                await channel.delete_messages(context_messages, command_message)
            else:
                interaction: hikari.CommandInteraction = ctx.interaction
                await interaction.delete_initial_response()
        return wrapper
    return decorator
