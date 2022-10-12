import json
from datetime import date

from dateparser import parse
from dateutil.rrule import MONTHLY, rrule
from scrapy.http import Request
from scrapy.selector import Selector

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RoPortoVelho(BaseGazetteSpider):
    TERRITORY_ID = "1100205"
    BASE_URL = "https://www.portovelho.ro.gov.br/dom/datatablearquivosmes/"

    name = "ro_porto_velho"
    allowed_domains = ["portovelho.ro.gov.br"]
    start_date = date(2007, 1, 1)

    def start_requests(self):
        end_date = self.end_date

        interval = rrule(MONTHLY, dtstart=self.start_date, until=end_date)[::-1]
        for _date in interval:
            yield Request(f"{self.BASE_URL}{_date.year}/{_date.month}")

    def parse(self, response):
        paragraphs = json.loads(response.text)["aaData"]

        for paragraph, *_ in paragraphs:
            selector = Selector(text=paragraph)
            url = selector.css("p a ::attr(href)").extract_first()

            text = selector.css("p strong ::text")
            is_extra_edition = text.extract_first().startswith("Suplemento")
            date = text.re_first(r"\d{1,2} de \w+ de \d{4}")

            # As datas estao vindo com os meses em ingles, de maneira que o parser se confunde
            # ao processar a data.
            date = date.replace("de", "of")
            date = parse(date).date()

            # O JSON retorna todos os arquivos de um determinado mes, mas so queremos de um
            # determinado periodo
            if date >= self.start_date and date <= self.end_date:
                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=is_extra_edition,
                    power="executive_legislative",
                )
