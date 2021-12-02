from cluefulbot.core.utils import utils
from lightbulb import context
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

            channel = ctx.get_channel()
            context_messages = [await response.message() for response in ctx.responses]
            command_message = ctx.event.message if utils.is_prefix_command(ctx) else None
            await channel.delete_messages(context_messages, command_message)
        return wrapper
    return decorator
