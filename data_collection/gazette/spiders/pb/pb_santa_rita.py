import re
from datetime import date, datetime

import scrapy
from dateutil.rrule import YEARLY, rrule
from scrapy.http import Response

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbSantaRitaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2513703"
    name = "pb_santa_rita"
    allowed_domains = ["santarita.pb.gov.br"]
    start_date = date(2013, 3, 28)

    def start_requests(self):
        for yearly_date in rrule(
            freq=YEARLY, dtstart=self.start_date, until=self.end_date
        ):
            url = f"https://santarita.pb.gov.br/diario-oficial/diario-oficial-{yearly_date.year}/"
            yield scrapy.Request(url, callback=self.parse_year)

    def parse_year(self, response):
        max_page = response.css(".search-pagination p span:nth-child(2)::text").get()

        for i in range(1, int(max_page) + 1):
            url = f"{response.url}page/{i}/"
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response: Response):
        gazzetes = response.css(".arq-list-item-content a")
        for gazzete in gazzetes:
            url = gazzete.attrib["href"]
            desc = gazzete.css("h1::text").get()

            raw_date = gazzete.css(".data::text").get().strip()
            date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            # URLs possuem diferentes padrões de enunciar o numero de edição
            # exemplos listados podem ser encontrados em https://regexr.com/7qsaa
            result = re.findall(
                "DOE-[Nn]?[o°]?-?(\d+A?)|(\d{1,3}A?)-DOE|n\.?-(\d{3,})-|OFICIAL-N?o?-?(\d{2,4}A?)|n_(\d+)|diario-(\d+)",
                url,
            )
            edition_number = max(result[0]) if result else None

            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[url],
                is_extra_edition="extra" in desc.lower(),
                power="executive_legislative",
            )
