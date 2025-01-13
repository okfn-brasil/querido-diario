import re
from datetime import date
from urllib.parse import urlparse

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MASaoLuisSpider(BaseGazetteSpider):
    name = "ma_sao_luis"
    TERRITORY_ID = "2111300"
    allowed_domains = ["diariooficial.saoluis.ma.gov.br"]
    start_urls = ["https://diariooficial.saoluis.ma.gov.br/diario-oficial"]
    start_date = date(1993, 1, 4)

    def parse(self, response, page=1):
        for item in response.css(".box-publicacao"):
            raw_infos = "".join(item.css("::text").getall()).strip()

            raw_edition_date = re.search(r",(.+)\s", raw_infos).group(1).strip()
            edition_date = dateparser.parse(raw_edition_date, languages=["pt"]).date()

            if self.start_date <= edition_date <= self.end_date:
                edition_number = re.search(r"(\d+)/", raw_infos).group(1)
                is_extra_edition = "extra" in raw_infos.lower()

                try:
                    edition_path = item.css("a")[1].attrib["href"]
                    edition_url = (
                        urlparse(self.start_urls[0])
                        ._replace(path=edition_path)
                        .geturl()
                    )
                except Exception:
                    self.logger.error(f"Unable to retrieve PDF URL for {edition_date}.")
                    continue

                yield Gazette(
                    date=edition_date,
                    edition_number=edition_number,
                    is_extra_edition=is_extra_edition,
                    file_urls=[edition_url],
                    power="executive_legislative",
                )

        last_page_number = int(response.css(".pagination .last a").attrib["data-page"])
        if edition_date > self.start_date and page < last_page_number:
            page += 1
            yield Request(
                f"https://diariooficial.saoluis.ma.gov.br/diario-oficial/index?page={page}",
                cb_kwargs={"page": page},
            )
