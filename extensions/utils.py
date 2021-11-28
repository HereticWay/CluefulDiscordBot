import hikari
import lightbulb
import datetime
import asyncio
from lightbulb import commands, context

utils_plugin = lightbulb.Plugin("Utils")


@utils_plugin.command
@lightbulb.option("target", "A channel to clear.", hikari.GuildChannel, required=False)
@lightbulb.option("count", "Number of messages to clear.", int, required=False)
@lightbulb.command("clear", "Clear messages from a channel.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def clear(ctx: context.Context) -> None:
    target_channel = ctx.options.target if (ctx.options.target is not None) else ctx.get_channel()
    clear_count = ctx.options.count if (ctx.options.count is not None) else 1

    deleted_messages_count = 0
    async with target_channel.trigger_typing():
        # Don't try to delete past two weeks
        now = datetime.datetime.utcnow()
        two_weeks_ago = now - datetime.timedelta(weeks=2)
        history = await target_channel.fetch_history(after=two_weeks_ago)
        history_trimmed = history[len(history)-clear_count-1:]

        deleted_messages_count = len(history_trimmed)
        await target_channel.delete_messages(history_trimmed)
    
    await ctx.respond(f"Deleted {deleted_messages_count} messages!")
    await asyncio.sleep(10)
    await ctx.delete_last_response()


@utils_plugin.command
@lightbulb.option("nickname", "Chosen nickname.", str, required=False)
@lightbulb.command("nickname", "Change your nickname.", aliases=["nick"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def nickname(ctx: context.Context) -> None:
    nick = ctx.options.nickname if (ctx.options.nickname is not None) else ""
    await ctx.member.edit(nick=nick)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utils_plugin)
