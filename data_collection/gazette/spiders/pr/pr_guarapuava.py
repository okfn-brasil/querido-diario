import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import YEARLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrGuarapuavaSpider(BaseGazetteSpider):
    name = "pr_guarapuava"
    TERRITORY_ID = "4109401"
    allowed_domains = ["guarapuava.pr.gov.br", "hmlpmg.plsscloud.com.br"]
    BASE_URL = "https://www.guarapuava.pr.gov.br/boletins-oficiais/{YEAR}-2/"
    start_date = date(2002, 1, 20)
    custom_settings = {"DOWNLOAD_DELAY": 0.5, "RANDOMIZE_DOWNLOAD_DELAY": True}

    def start_requests(self):
        for yearly_date in rrule(
            freq=YEARLY, dtstart=self.start_date, until=self.end_date
        ):
            url = self.BASE_URL.format(YEAR=yearly_date.year)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = response.css(".item .link a")
        for item in items:
            if not self.is_valid_item(item):
                continue

            yield Gazette(
                date=self.gazette_date(item),
                edition_number=self.gazette_edition(item),
                file_urls=[item.attrib["href"]],
                is_extra_edition=self.gazette_extra_edition(item),
                power="executive_legislative",
            )

    def is_valid_item(self, item):
        # Lidando com erros no HTML da página. Exemplo:
        # https://www.guarapuava.pr.gov.br/boletins-oficiais/2020-2/
        if not self.gazette_edition(item) and not item.attrib["href"]:
            return False
        # Boletim sem data não possuem arquivos disponíveis. Exemplo:
        # https://www.guarapuava.pr.gov.br/boletins-oficiais/2011-2/
        if not self.gazette_date(item):
            return False
        return True

    def gazette_edition(self, item):
        desc = self.gazette_description(item)
        match = re.findall("oficial {1,}(\d+).+", desc)
        return match[0] if match else None

    def gazette_date(self, item):
        desc = self.gazette_description(item)
        dates = re.findall("(\d{2}/\d{2}/\d{4})", desc)
        if not dates:
            return None
        return datetime.strptime(dates[-1], "%d/%m/%Y").date()

    def gazette_extra_edition(self, item):
        desc = self.gazette_description(item)
        return "extra" in desc or "parte ii" in desc

    def gazette_description(self, item):
        desc = item.css("::text").get()
        return str(desc).lower()
