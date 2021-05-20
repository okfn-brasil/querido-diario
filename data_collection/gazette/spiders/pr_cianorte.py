from dateparser import parse
from scrapy.http import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrCianorteSpider(BaseGazetteSpider):
    TERRITORY_ID = "4105508"
    name = "pr_cianorte"
    allowed_domains = ["cianorte.pr.gov.br"]
    start_urls = ["https://cianorte.pr.gov.br/orgao-oficial/"]

    def parse(self, response, current_page=1):
        lines = response.css("tbody tr")
        if not lines:
            return

        for row in lines:
            date = row.xpath("td[2]/text()").get()
            edition_number = row.xpath("td[1]/text()").get()

            yield Gazette(
                date=parse(date, languages=["pt"]).date(),
                edition_number=edition_number,
                file_urls=row.xpath("td[3]/a/@href").getall(),
                is_extra_edition=False,
                power="executive_legislative",
            )
        yield Request(
            f"https://cianorte.pr.gov.br/orgao-oficial/pagina/{str(current_page)}",
            cb_kwargs=dict(current_page=current_page + 1),
        )
