from concurrent.futures import ProcessPoolExecutor
from cluefulbot.core.utils import youtube_downloader
from lightbulb import commands, context
import asyncio
import lightbulb

youtube_plugin = lightbulb.Plugin("Utils")


@youtube_plugin.command
@lightbulb.option(name="url", description="The url of the music you want to download", type=str, required=True)
@lightbulb.command(name="ytdl", description="Download music from Youtube")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def ytdl(ctx: context.Context):
    channel = ctx.get_channel()
    url = ctx.options.url  # TODO: Implement url format checking too

    await ctx.respond("Downloading music...")
    async with channel.trigger_typing():
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=1) as executor:
            success, file_name = await loop.run_in_executor(
                executor,
                youtube_downloader.download_mp3,
                url
            )

        if success:
            await ctx.edit_last_response(":white_check_mark: Download succeeded! :slight_smile: Now uploading the file...")
            async with channel.trigger_typing():
                await ctx.edit_last_response("Here it is: ", attachment=file_name)  # FIXME: Fix common timeout error!
        else:
            await ctx.edit_last_response(":no_entry: Download failed! :confused:")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(youtube_plugin)
