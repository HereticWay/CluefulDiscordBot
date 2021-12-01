from lightbulb import context


def is_prefix_command(ctx: context.Context):
    return ctx.interaction is None
