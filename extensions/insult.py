import hikari
import lightbulb
from lightbulb import commands, context
import aiohttp

info_plugin = lightbulb.Plugin("Insult")


class InsultApiError(Exception):
    pass


@info_plugin.command
@lightbulb.option("target", "A member to insult.", hikari.User, required=False)
@lightbulb.command("insult", "Insult a member for good.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def insult(ctx: context.Context) -> None:
    target = ctx.options.target if (ctx.options.target is not None) else ctx.user
    try:
        random_insult = await get_random_insult()
    except InsultApiError:
        random_insult = """🦆 you!"""
    await target.reply(random_insult)


async def get_random_insult():
    'Gets a random insult asynchronously using the EvilInsult API'
    async with aiohttp.ClientSession() as client:
        async with client.get('https://evilinsult.com/generate_insult.php') as response:
            if not response.status == 200:
                raise InsultApiError

            return await response.text()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)
