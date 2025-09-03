import re
from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjVarreSaiSpider(BaseGazetteSpider):
    name = "rj_varre_sai"
    TERRITORY_ID = "3306156"
    start_date = date(2019, 9, 21)
    allowed_domains = ["dados.varresai.rj.gov.br"]
    start_urls = ["https://varresai.rj.gov.br/diarios-oficiais/"]

    def parse(self, response):
        script_content = response.xpath(
            '//script[contains(text(), "window.__NUXT__")]/text()'
        ).get()
        match = re.search(r'key:"([^"]+)"', script_content)
        if match:
            key_value = match.group(1)
            headers = {"key": key_value, "content-type": "application/json"}
            url = "https://dados.varresai.rj.gov.br/api/diarios-oficiais/lista/simples"
            yield scrapy.Request(url=url, headers=headers, callback=self.gazette_parse)

    def gazette_parse(self, response):
        for gazette in response.json()["payload"]:
            gazette_date = datetime.strptime(
                gazette["data_publicacao"][:10], "%Y-%m-%d"
            ).date()
            if gazette_date > self.end_date:
                continue

            if gazette_date < self.start_date:
                return

            edition_number = gazette["numero"].lstrip("0")
            url = response.urljoin(gazette["arquivo"])

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                file_urls=[url],
                power="executive_legislative",
            )
