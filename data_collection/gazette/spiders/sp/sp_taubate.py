import re
from datetime import date, datetime

from dateutil.rrule import DAILY, rrule
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpTaubaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3554102"
    name = "sp_taubate"
    allowed_domains = ["plenussistemas.dioenet.com.br"]
    base_url = "https://plenussistemas.dioenet.com.br/list/taubate?secao="
    start_date = date(2022, 12, 8)

    def start_requests(self):
        for daily_date in rrule(
            freq=DAILY, dtstart=self.start_date, until=self.end_date
        ):
            yield Request(f'{self.base_url}&d={daily_date.strftime("%d/%m/%Y")}')

    def parse(self, response):
        for gazzete in response.css("ul.lista-diarios li"):
            desc = gazzete.css(".col-one span::text").get()
            gazzete_number = re.findall("\d+", desc)[0]

            elem = gazzete.css(".col-two a.btn")
            gazzete_url = elem.attrib["href"]
            raw_date = re.findall("(\d{2}/\d{2}/\d{4})", elem.attrib["title"])[0]
            gazzete_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            yield Gazette(
                date=gazzete_date,
                edition_number=gazzete_number,
                is_extra_edition=False,
                power="executive_legislative",
                file_urls=[gazzete_url],
            )
