import datetime as dt
import json

from dateparser import parse
from scrapy import Request, Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class RoPortoVelho(BaseGazetteSpider):
    TERRITORY_ID = "1100205"
    BASE_URL = "https://www.portovelho.ro.gov.br/dom/datatablearquivosmes/"
    start_date = dt.datetime(2007, 1, 1)

    name = "ro_porto_velho"
    allowed_domains = ["portovelho.ro.gov.br"]

    def start_requests(self):
        for date in monthly_sequence(self.start_date, self.end_date, format="%Y/%m")[
            ::-1
        ]:
            print(f"{self.BASE_URL}{date}")
            yield Request(f"{self.BASE_URL}{date}")

    def parse(self, response):
        paragraphs = json.loads(response.body_as_unicode())["aaData"]
        for paragraph, *_ in paragraphs:
            selector = Selector(text=paragraph)
            url = selector.css("p a ::attr(href)").extract_first()

            text = selector.css("p strong ::text")
            is_extra_edition = text.extract_first().startswith("Suplemento")
            date = text.re_first(r"\d{1,2} de \w+ de \d{4}")
            date = parse(date, languages=["pt"]).date()

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )
