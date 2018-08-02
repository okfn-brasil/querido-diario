import datetime as dt
import json

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RrBoaVistaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1400100"
    name = "rr_boa_vista"
    allowed_domains = ["boavista.rr.gov.br"]
    start_urls = ["https://www.boavista.rr.gov.br/diario-oficial"]

    def parse(self, response):
        options = response.xpath('//*[@id="Periodo"]/optgroup/option/@value')
        for option in options:
            data = option.extract()

            url = "".join([self.start_urls[0], "?Periodo=", data])
            yield scrapy.Request(url, self.parse_period)

    def parse_period(self, response):
        items = []
        div_list = response.xpath('//*[@class="bldownload"]')
        for div in div_list:
            content = div.xpath("./div/text()").extract()
            date = parse(content[1], languages=["pt"]).date()

            url = div.xpath("./a/@href").extract_first()
            url = response.urljoin(url)

            power = "executive_legislature"
            items.append(
                Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=False,
                    territory_id=self.TERRITORY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow(),
                ))

        return items
