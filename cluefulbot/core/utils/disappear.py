from cluefulbot.core.utils import utils
from lightbulb import context
import asyncio
import functools


def disappear(after: int):
    """Decorator to make a command's context disappear after the given number of seconds.

    Args:
        after (int): number of seconds to disappear
    """
    def decorator(fnc):
        @functools.wraps(fnc)
        async def wrapper(ctx: context.Context):
            await fnc(ctx)

            channel = ctx.get_channel()
            context_messages = [await response.message() for response in ctx.responses]
            command_message = ctx.event.message if utils.is_prefix_command(ctx) else None
            await asyncio.sleep(after)
            await channel.delete_messages(context_messages, command_message)
        return wrapper
    return decorator
