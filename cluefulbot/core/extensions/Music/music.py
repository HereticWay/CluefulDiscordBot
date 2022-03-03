import hikari
import lavasnek_rs
import lightbulb
from lightbulb import commands, context
from cluefulbot.core.utils.config import *

music_plugin = lightbulb.Plugin("Music")


class EventHandler:
    async def track_start(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        pass

    async def track_finish(self, _: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        pass

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:

        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)


@music_plugin.listener(hikari.ShardReadyEvent)
async def on_shard_ready(event: hikari.ShardReadyEvent):
    builder = lavasnek_rs.LavalinkBuilder(event.my_user.id, get_token())
    builder.set_host(get_lavalink_host())
    builder.set_password(get_lavalink_password())

    music_plugin.bot.d.lavalink = await builder.build(EventHandler())


@music_plugin.command
@lightbulb.command("join", "Join the bot to the voice channel you are in.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _join(ctx: lightbulb.Context) -> None:
    voice_states_view = music_plugin.app.cache.get_voice_states_view_for_guild(ctx.guild_id)
    user_voice_state = [state async for state in voice_states_view.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not user_voice_state:
        await ctx.respond("You're not connected to any voice server!")
        return

    channel_id = user_voice_state[0].channel_id
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d.lavalink
    try:
        connection_info = await lavalink.join(ctx.guild_id, channel_id)
    except TimeoutError:
        await ctx.respond("Could not connect to the voice channel :sad:")
        return

    await lavalink.create_session(connection_info)
    await ctx.respond(f"Joined <#{channel_id}>!")


@music_plugin.command
@lightbulb.command("leave", "Leave the voice channel the bot currently in")
@lightbulb.implements(lightbulb.SlashCommand)
async def _leave(ctx: lightbulb.Context) -> None:
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d.lavalink
    await lavalink.destroy(ctx.guild_id)
    await lavalink.leave(ctx.guild_id)
    await lavalink.remove_guild_node(ctx.guild_id)
    await lavalink.remove_guild_from_loops(ctx.guild_id)

    await ctx.respond(f"Left <#{ctx.channel_id}>!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(music_plugin)
