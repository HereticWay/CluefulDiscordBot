from urllib.error import HTTPError
import logging as log
import lightbulb
from lightbulb.ext import tasks
from cluefulbot.core.utils.ad_manager import AdManager

adwatch_plugin = lightbulb.Plugin("AdWatch")
HARDVERAPRO_CHANNEL_ID = 1042767606454697996
AD_WATCH_REFRESH_INTERVAL = 15 # minutes
AD_WATCH_MAX_CONSECUTIVE_FAILURES = 100


@tasks.task(m=AD_WATCH_REFRESH_INTERVAL, auto_start=True, pass_app=True, wait_before_execution=False, max_consecutive_failures=AD_WATCH_MAX_CONSECUTIVE_FAILURES)
async def refresh_adwatch(bot: lightbulb.BotApp) -> None:
    if not bot.d.ad_manager:
        bot.d.ad_manager = AdManager()

    ad_manager = bot.d.ad_manager

    try:
        new_ads = ad_manager.update_ads_and_return_new_ones()
    except HTTPError:
        log.exception("There was an HTTP error during ads list refresh.")

    if new_ads:
        for ad in new_ads:
            await bot.rest.create_message(HARDVERAPRO_CHANNEL_ID, f'{ad.title}; {ad.price}; From: {ad.seller_name}; Link: {ad.link}')
            log.info('New ad sent to the channel!')
        ad_manager.save_ads()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(adwatch_plugin)
