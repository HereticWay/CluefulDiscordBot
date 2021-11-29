import hikari
import lightbulb
from lightbulb import commands, context
from html import unescape
import unicodedata
import aiohttp

insult_plugin = lightbulb.Plugin("Insult")


class InsultApiError(Exception):
    pass


@insult_plugin.command
@lightbulb.option(name="target", description="A member to insult.", type=hikari.User, required=False)
@lightbulb.command(name="insult", description="Insult a member for good.")
@lightbulb.implements(commands.SlashCommand)
async def insult(ctx: context.Context) -> None:
    target = ctx.options.target if (ctx.options.target is not None) else ctx.user
    try:
        random_insult = handle_html_entities(await get_random_insult())
    except InsultApiError:
        random_insult = ":duck: you!"
    await ctx.respond(f"{target.mention} {random_insult}")


def handle_html_entities(text: str) -> str:
    unescaped_text = unescape(text)
    return unicodedata.normalize('NFKC', unescaped_text)


async def get_random_insult() -> str:
    """Gets a random insult asynchronously using the EvilInsult API"""
    async with aiohttp.ClientSession() as client:
        async with client.get('https://evilinsult.com/generate_insult.php') as response:
            if not response.status == 200:
                raise InsultApiError

            return await response.text()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(insult_plugin)
