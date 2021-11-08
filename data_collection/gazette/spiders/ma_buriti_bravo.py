from datetime import date, datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaBuritiBravoSpider(BaseGazetteSpider):

    name = "ma_buriti_bravo"
    allowed_domains = ["diario.buritibravo.ma.gov.br"]
    start_date = date(2018, 11, 26)
    url_base = "http://diario.buritibravo.ma.gov.br/publicacao/selecionar.php"
    TERRITORY_ID = "2102200"

    def start_requests(self):
        yield scrapy.Request(self.url_base, callback=self.parse_page)

    def parse_page(self, response):
        last_page = int(
            response.xpath("//div[@class='paginacao']/a[last()]/span/text()").get()
        )
        for page in range(0, last_page):
            yield scrapy.FormRequest(
                url=response.url, method="POST", formdata={"pag": str(page)}
            )

    def parse(self, response):
        lines = response.xpath("//table/tbody/tr")

        for line in lines:
            try:
                date = datetime.strptime(line.xpath("td[3]/text()").get(), "%d/%m/%Y")
            except ValueError:
                continue
            except TypeError:
                continue
            file_url = response.urljoin(line.xpath("td[5]/a/@href").get())
            edition_number = line.xpath("td[4]/text()").re_first(r"\d+")

            yield Gazette(
                date=date.date(),
                file_urls=[file_url],
                edition_number=edition_number,
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power="executive",
                scraped_at=datetime.utcnow(),
            )
