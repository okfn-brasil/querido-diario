import datetime as dt

from dateparser import parse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgItaunaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3133808"
    name = "mg_itauna"
    allowed_domains = ["itauna.mg.gov.br"]
    start_urls = ["https://www.itauna.mg.gov.br/portal/diario-oficial/"]

    def parse(self, response):
        diarios = response.xpath("//div[@class='d_e_modelo_diario']")
        for diario in diarios:
            url = (
                "https://www.itauna.mg.gov.br"
                + diario.css("a")[1].extract().split('"')[1]
            )
            date = diario.xpath("div/span/text()").extract()[0].split()[0]
            is_extra_edition = True if len(diario.css("i")) == 4 else False
            yield Gazette(
                date=parse(date, languages=["pt"]).date(),
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                territory_id=self.TERRITORY_ID,
                power="executive_legislature",
                scraped_at=dt.datetime.utcnow(),
            )
        url = "https://www.itauna.mg.gov.br/portal/diario-oficial/{i}/0/0/0/0/"
        last_page = int(response.xpath("//select/option/text()")[-1].extract())
        for i in range(1, 1 + last_page):
            yield Request(url.format(i=i), callback=self.parse)
