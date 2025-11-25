import datetime as dt
import re
from datetime import date

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpBarueriSpider(BaseGazetteSpider):
    name = "sp_barueri"
    TERRITORY_ID = "3505708"
    allowed_domains = ["portal.barueri.sp.gov.br"]
    PAGINATION_URL = "https://portal.barueri.sp.gov.br/Diario/CbkOutrosDiarios"
    start_urls = ["https://portal.barueri.sp.gov.br/diario"]
    EDITION_NUMBER_REGEX = re.compile(r"Edição\s+(\d+)")
    start_date = date(2010, 1, 6)

    def parse(self, response):
        follow_next_page = True
        current_page = response.xpath(
            '//div[contains(@class, "pagination")]//select/option[@selected]/@value'
        ).get()

        if current_page == "1":
            recentGazettes = response.xpath(
                "//div[contains(@class, 'container') and contains(@class, 'container-diario')]"
            )
            for gazette in recentGazettes:
                raw_date = gazette.xpath(
                    ".//div[contains(@class, 'diarioTopoText')][1]//b/text()"
                ).get()
                date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

                if date < self.start_date:
                    follow_next_page = False
                    break

                if date > self.end_date:
                    continue

                edition_number = gazette.xpath(
                    ".//div[contains(@class, 'diarioTopoText')][2]/text()"
                ).get()
                url = gazette.xpath(
                    ".//a[contains(@class, 'acessarJornal')]/@href"
                ).get()
                distribution = gazette.xpath(
                    ".//div[contains(@class, 'diarioTopoText')][4]/text()"
                ).get()
                is_extra_edition = "extraordinária" in distribution.lower()

                item = Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=is_extra_edition,
                    power="executive_legislative",
                    edition_number=edition_number,
                )
                yield item

        gazettes = response.xpath('//table[contains(@class, "OutrosDiarios")]//tr')
        for gazette in gazettes:
            raw_date = gazette.xpath("./td/div/b/text()").get()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

            if date < self.start_date:
                follow_next_page = False
                break

            if date > self.end_date:
                continue

            url = gazette.xpath("./td/a/@href").get()
            text = gazette.xpath("./td/div[2]/text()").get()
            edition_number = int(self.EDITION_NUMBER_REGEX.search(text).group(1))
            is_extra_edition = "extraordinária" in text.lower()

            item = Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
                edition_number=edition_number,
            )
            yield item

        if follow_next_page:
            page_options = response.xpath(
                '//div[contains(@class, "pagination")]//select/option/@value'
            ).getall()
            next_page = str(int(current_page) + 1)
            if next_page in page_options:
                formdata = {"pagina": str(next_page)}
                yield scrapy.FormRequest(
                    url=self.PAGINATION_URL,
                    formdata=formdata,
                    callback=self.parse,
                    method="POST",
                )
