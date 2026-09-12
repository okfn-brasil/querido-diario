import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjItaguaiSpider(BaseGazetteSpider):
    name = "rj_itaguai"
    TERRITORY_ID = "3302007"
    allowed_domains = ["www.attosoficiais.com.br"]
    start_date = dt.date(2013, 2, 19)
    power = "executive_legislative"

    editions_url = "https://www.attosoficiais.com.br/edicoes.json"

    async def start(self):
        yield scrapy.Request(self.editions_url)

    def parse(self, response):
        for edition in response.json():
            raw_date = edition.get("data")
            if raw_date is None:
                continue

            edition_date = dt.date.fromisoformat(raw_date)
            if not self.start_date <= edition_date <= self.end_date:
                continue

            yield Gazette(
                date=edition_date,
                edition_number=str(edition["numero"]),
                file_urls=[response.urljoin(edition["arquivo"])],
                is_extra_edition="extra" in edition["nome"].lower(),
                power=self.power,
            )
