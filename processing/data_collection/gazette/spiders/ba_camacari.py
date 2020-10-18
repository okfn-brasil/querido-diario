import re
import datetime
from urllib.parse import urlencode

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaCamacari(BaseGazetteSpider):
    TERRITORY_ID = "2905701"
    BASE_URL = "http://www.camacari.ba.gov.br/wp-content/themes/camacari/assets/ajax/arquivos.php"
    name = "ba_camacari"
    allowed_domains = ["camacari.ba.gov.br"]
    start_date = datetime.date(2007, 10, 10)

    FILE_SELECTOR = ".mb-40 a::attr(href)"
    TITLE_SELECTOR = ".mb-40 a::text"
    EXTRA_EDITION_REGEX = r"EXTRA"
    EDITION_NUMBER_REGEX = r"\d+"
    DATE_SELECTOR = ".mb-10::text"
    DATE_REGEX = r"\d+\/\d+\/\d+"
    DOCUMENT_SELECTOR = ".col-sm-12"

    def start_requests(self):
        params = {"paged": 1, "categoria": "diario-oficial"}
        url = f"{self.BASE_URL}?{urlencode(params)}"
        yield scrapy.Request(url=url, callback=self.parse, meta={"params": params})

    def parse(self, response):
        document_list = response.css(self.DOCUMENT_SELECTOR)
        last_scraped_gazette_date = datetime.date.today()

        for document in document_list:
            date_text = document.css(self.DATE_SELECTOR).re_first(self.DATE_REGEX)
            date = dateparser.parse(date_text, languages=["pt"]).date()

            file_url = document.css(self.FILE_SELECTOR).get()

            title = document.css(self.TITLE_SELECTOR).get()
            edition_number = re.search(
                self.EDITION_NUMBER_REGEX, title.replace(".", "")
            ).group(0)
            is_extra_edition = bool(
                re.search(self.EXTRA_EDITION_REGEX, title, re.IGNORECASE)
            )

            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=datetime.datetime.utcnow(),
                edition_number=edition_number,
            )

            last_scraped_gazette_date = date

        if document_list and self.start_date <= last_scraped_gazette_date:
            next_params = response.meta["params"]
            next_params["paged"] += 1
            next_url = f"{self.BASE_URL}?{urlencode(next_params)}"
            yield scrapy.Request(
                url=next_url, callback=self.parse, meta={"params": next_params}
            )
