import hikari
import lightbulb
from datetime import datetime, timedelta
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

    async with target_channel.trigger_typing():
        now = datetime.utcnow()
        two_weeks_ago = now - timedelta(weeks=2)
        history = await target_channel.fetch_history(after=two_weeks_ago)
        history_limited = history[-clear_count-1:]

        deleted_messages_count = len(history_limited)
        await target_channel.delete_messages(history_limited)
    
    sent_message = await ctx.respond(f"Deleted {deleted_messages_count} messages!")
    await asyncio.sleep(10)
    await sent_message.delete()


@utils_plugin.command
@lightbulb.option("nickname", "Chosen nickname.", str, required=False)
@lightbulb.command("nickname", "Change your nickname.", aliases=["nick"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def nickname(ctx: context.Context) -> None:
    nick = ctx.options.nickname if (ctx.options.nickname is not None) else ""
    await ctx.member.edit(nick=nick)


@utils_plugin.command
@lightbulb.command("serverstats", "Get stats of the server.")
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
        

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utils_plugin)
