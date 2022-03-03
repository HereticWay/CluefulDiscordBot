import hikari
import lavasnek_rs
import lightbulb
from cluefulbot.core.utils.config import *

music_plugin = lightbulb.Plugin("Music")


class EventHandler:
    async def stats(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.Stats) -> None:
        pass

    async def player_update(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.PlayerUpdate) -> None:
        pass

    async def track_start(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStart) -> None:
        pass

    async def track_finish(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackFinish) -> None:
        pass

    async def track_exception(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackException) -> None:
        # If a track was unable to be played, skip it
        skip = await lavalink.skip(event.guild_id)
        node = await lavalink.get_guild_node(event.guild_id)

        if not node:
            return

        if skip and not node.queue and not node.now_playing:
            await lavalink.stop(event.guild_id)

    async def track_stuck(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.TrackStuck) -> None:
        pass

    async def websocket_closed(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.WebSocketClosed) -> None:
        pass

    async def player_destroyed(self, lavalink: lavasnek_rs.Lavalink, event: lavasnek_rs.PlayerDestroyed) -> None:
        pass


@music_plugin.listener(hikari.ShardReadyEvent)
async def on_shard_ready(event: hikari.ShardReadyEvent) -> None:
    builder = lavasnek_rs.LavalinkBuilder(event.my_user.id, get_token())
    builder.set_host(get_lavalink_host())
    builder.set_password(get_lavalink_password())

    music_plugin.bot.d["lavalink"] = await builder.build(EventHandler())


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("join", "Join the bot to the voice channel you are in.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _join(ctx: lightbulb.Context) -> None:
    voice_states_view = music_plugin.app.cache.get_voice_states_view_for_guild(ctx.guild_id)
    user_voice_state = [state async for state in
                        voice_states_view.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not user_voice_state:
        await ctx.respond("You're not connected to any voice server!")
        return

    channel_id = user_voice_state[0].channel_id
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]
    try:
        connection_info = await lavalink.join(ctx.guild_id, channel_id)
    except TimeoutError:
        await ctx.respond("Could not connect to the voice channel :sad:")
        return

    await lavalink.create_session(connection_info)
    await ctx.respond(f"Joined <#{channel_id}>!")


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("leave", "Leave the voice channel the bot currently in")
@lightbulb.implements(lightbulb.SlashCommand)
async def _leave(ctx: lightbulb.Context) -> None:
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]
    await lavalink.destroy(ctx.guild_id)
    await lavalink.leave(ctx.guild_id)
    await lavalink.remove_guild_node(ctx.guild_id)
    await lavalink.remove_guild_from_loops(ctx.guild_id)

    await ctx.respond(f"Left <#{ctx.channel_id}>!")


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.option("query", "Url or name of the song to play.")
@lightbulb.command("play", "Adds the given url/queried song to the queue.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _play(ctx: lightbulb.Context) -> None:
    query = ctx.options.query
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]

    query_info = await lavalink.search_tracks(query)
    if not query_info.tracks:
        await ctx.respond("Couldn't find this song!")
        return

    track = query_info.tracks[0]
    play_builder = lavalink.play(ctx.guild_id, track)
    play_builder.requester(ctx.author.id)
    try:
        await play_builder.queue()
    except lavasnek_rs.NoSessionPresent:
        await ctx.respond("Use '/join' first!")

    await ctx.respond(f"Added to queue: {track.info.title}")


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("stop", "Stops the music player.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _stop(ctx: lightbulb.Context) -> None:
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]

    await lavalink.stop(ctx.guild_id)
    await ctx.respond("Stopped the queue!")


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("skip", "Skips one song on the queue.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _skip(ctx: lightbulb.Context) -> None:
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]
    track_queue: lavasnek_rs.TrackQueue = await lavalink.skip(ctx.guild_id)
    node: lavasnek_rs.Node = await lavalink.get_guild_node(ctx.guild_id)

    if not track_queue:
        await ctx.respond("There's nothing to skip.")
        return

    if not node.queue and not node.now_playing:
        await lavalink.stop(ctx.guild_id)

    await ctx.respond(f"Skipped: {track_queue.track.info.title}.")


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("pause", "Pauses the player.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _pause(ctx: lightbulb.Context) -> None:
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]
    await lavalink.pause(ctx.guild_id)
    await ctx.respond("Player paused!")


@music_plugin.command
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command("resume", "Resumes the player.")
@lightbulb.implements(lightbulb.SlashCommand)
async def _resume(ctx: lightbulb.Context) -> None:
    lavalink: lavasnek_rs.Lavalink = music_plugin.bot.d["lavalink"]
    await lavalink.resume(ctx.guild_id)
    await ctx.respond("Player resumed!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(music_plugin)
