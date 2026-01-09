import re
from datetime import date

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjValencaSpider(BaseGazetteSpider):
    name = "rj_valenca"
    TERRITORY_ID = "3306107"
    allowed_domains = ["valenca.rj.gov.br"]
    start_urls = ["https://valenca.rj.gov.br/boletins-oficiais/"]
    start_date = date(2011, 1, 1)

    def parse(self, response):
        gazettes = response.xpath('//div[@class="accordionContent"]//a')

        for gazette in gazettes:
            title = gazette.xpath("text()").get("").strip()
            file_url = gazette.xpath("@href").get()

            match = re.search(
                r"n[°º\.]*\s*([\d\.]+)\s*–\s*(\d{1,2} de [A-Za-z]+ de \d{4})",
                title,
                flags=re.IGNORECASE,
            )
            if not match:
                continue

            edition_number = match.group(1).replace(".", "")
            gazette_date_str = match.group(2)

            gazette_date = dateparser.parse(gazette_date_str, languages=["pt"])
            if gazette_date:
                gazette_date = gazette_date.date()
            else:
                continue

            if gazette_date > self.end_date:
                continue

            if gazette_date < self.start_date:
                return

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[file_url],
                is_extra_edition=False,
                power="executive_legislative",
            )
