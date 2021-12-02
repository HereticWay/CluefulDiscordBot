import hikari
import lightbulb
from datetime import datetime, timedelta, timezone
from lightbulb import commands, context
from cluefulbot.core.utils.disappear import disappear
from cluefulbot.core.utils import utils
from hikari import iterators
from hikari import messages

utils_plugin = lightbulb.Plugin("Utils")


@utils_plugin.command
@lightbulb.option(name="target", description="A channel to clear.", type=hikari.GuildChannel, required=False)
@lightbulb.option(name="count", description="Number of messages to clear.", type=int, required=False)
@lightbulb.command(name="clear", description="Clear messages from a channel.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
@disappear(after=10)
async def clear(ctx: context.Context) -> None:
    target_channel = ctx.options.target if (ctx.options.target is not None) else ctx.get_channel()
    clear_count = ctx.options.count if (ctx.options.count is not None) else 1

    async with target_channel.trigger_typing():
        command = ctx.event.message if utils.is_prefix_command(ctx) else ctx.interaction

        two_weeks_ago = datetime.now(timezone.utc) - timedelta(weeks=2)
        history_iterator = target_channel.fetch_history(before=command) \
            .limit(clear_count) \
            .take_while(lambda msg: two_weeks_ago < msg.created_at)

        history = frozenset([message async for message in history_iterator])
        await target_channel.delete_messages(history)

    await ctx.respond(f"Deleted {len(history)} message(s)!")


@utils_plugin.command
@lightbulb.option(name="nickname", description="Chosen nickname.", type=str, required=False)
@lightbulb.command(name="nickname", description="Change your nickname.", aliases=["nick"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
@disappear(after=10)
async def nickname(ctx: context.Context) -> None:
    nick = ctx.options.nickname if (ctx.options.nickname is not None) else ""
    is_prefix_command = (ctx.interaction is None)

    try:
        await ctx.member.edit(nick=nick)
        sent_message = await ctx.respond(f"Nickname changed to {nick}.", reply=True)
    except hikari.ForbiddenError:
        sent_message = await ctx.respond("Could not change your nickname.", reply=True)


@utils_plugin.command
@lightbulb.command(name="serverstats", description="Get stats of the server.")
@lightbulb.implements(commands.SlashCommand)
async def stats(ctx: context.Context) -> None:
    guild = ctx.get_guild()
    roles = await guild.fetch_roles()
    usable_roles = roles[1:]

    members = guild.get_members()
    dicts = {}

    for role in usable_roles:
        dicts[role.id] = 0

    for member in members:
        members_roles = guild.get_member(member).role_ids
        for role_id in members_roles:
            if role_id in dicts.keys():
                dicts[role_id] += 1

    embed = (
        hikari.Embed(
            title=f"{guild.name}",
            description="Server Stats",
            colour=0xFF793B,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(guild.banner_url)
    )

    for key, value in dicts.items():
        embed.add_field(
            f"{value} has",
            f"{guild.get_role(key).mention}",
            inline=True
        )

    await ctx.respond(embed)


@utils_plugin.command
@lightbulb.command(name="ping", description="The bot's ping")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def ping(ctx: context.Context) -> None:
    await ctx.respond(f"Pong! Latency: {ctx.bot.heartbeat_latency * 1000:.2f}ms")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utils_plugin)
