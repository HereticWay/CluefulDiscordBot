from lightbulb import context


def is_prefix_command(ctx: context.Context) -> bool:
    """Returns if the given context is using prefix commands

    Args:
        ctx (context.Context): the context of the command

    Returns:
        bool: True if the context is a PrefixCommand. False if it's a SlashCommand.
    """
    return ctx.interaction is None
