import asyncio
from datetime import datetime

import hikari
import lightbulb
from lightbulb import commands, context

utils_plugin = lightbulb.Plugin("Utils")


@utils_plugin.command
@lightbulb.option(name="target", description="A channel to clear.", type=hikari.GuildChannel, required=False)
@lightbulb.option(name="count", description="Number of messages to clear.", type=int, required=False)
@lightbulb.command(name="clear", description="Clear messages from a channel.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def clear(ctx: context.Context) -> None:
    target_channel = ctx.options.target if (ctx.options.target is not None) else ctx.get_channel()
    clear_count = ctx.options.count if (ctx.options.count is not None) else 1

    # TODO: Implement clear functionality
    # async with target_channel.trigger_typing():

    sent_message = await ctx.respond(f"Not implemented yet!")
    await asyncio.sleep(10)
    await sent_message.delete()


@utils_plugin.command
@lightbulb.option(name="nickname", description="Chosen nickname.", type=str, required=False)
@lightbulb.command(name="nickname", description="Change your nickname.", aliases=["nick"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def nickname(ctx: context.Context) -> None:
    nick = ctx.options.nickname if (ctx.options.nickname is not None) else ""
    try:
        await ctx.member.edit(nick=nick)
        sent_message = await ctx.respond(f"Nickname changed to {nick}.", reply=True)
        await asyncio.sleep(10)
        await sent_message.delete()
        await ctx.event.message.delete()
    except:
        
        sent_message = await ctx.respond(f"Could not change your nickname.", reply=True)
        await asyncio.sleep(10)
        await sent_message.delete()
        await ctx.event.message.delete()


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
            description=f"Server Stats",
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
