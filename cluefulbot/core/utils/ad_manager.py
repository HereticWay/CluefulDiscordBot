from os import path
import os
import json
from cluefulbot.core.utils.ad_extractor import AdExtractor, Ad, AdJSONEncoder

ADS_FILE = './ads.json'


class AdWatchUrlNotDefinedException(Exception):
    pass


class AdManager:
    __slots__ = (
        'ads',
        'ad_extractor'
    )

    def __init__(self) -> None:
        self.ads = self.load_ads() or []
        self.ad_extractor = AdExtractor(url=self.load_url())

    def load_ads(self) -> list[Ad] | None:
        if not path.exists(ADS_FILE):
            return None

        ads: list[Ad] = []
        with open(ADS_FILE, 'r') as file:
            for ad_dict in json.loads(file.readline()):
                ads.append(Ad(**ad_dict))
        return ads

    def load_url(self) -> str:
        adwatch_url = os.getenv('ADWATCH_URL')
        if not adwatch_url:
            raise AdWatchUrlNotDefinedException()

        return adwatch_url

    def save_ads(self) -> None:
        with open(ADS_FILE, 'w') as file:
            file.write(json.dumps(self.ads, cls=AdJSONEncoder))

    def update_ads_and_return_new_ones(self) -> list[Ad]:
        ads = self.ad_extractor.get_ads()

        new_ads: list[Ad] = [ad for ad in ads if ad not in self.ads]
        self.ads = ads

        return new_ads

