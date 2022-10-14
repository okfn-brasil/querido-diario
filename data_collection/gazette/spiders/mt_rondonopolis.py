import datetime

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MtRondonopolisSpider(BaseGazetteSpider):
    TERRITORY_ID = "5107602"
    name = "mt_rondonopolis"
    allowed_domains = ["rondonopolis.mt.gov.br/"]
    start_urls = ["http://www.rondonopolis.mt.gov.br/diario-oficial/"]

    start_date = datetime.date(2022, 10, 10)

    def parse(self, response):

        for gazette in response.css("tbody tr"):
            edicao = gazette.css("td:first-child::text").get()

            data = gazette.xpath('td[contains(text(), "/")]//text()').get()
            parsed_data = datetime.datetime.strptime(data, "%d/%m/%y").date()

            if self.start_date > parsed_data:
                break

            pdf_urls = response.urljoin(gazette.css("td a::attr(href)").get())

            yield Gazette(
                file_urls=[pdf_urls],
                date=parsed_data,
                power="executive",
                is_extra_edition=False,
                edition_number=edicao,
            )
