import datetime as dt

import scrapy

from gazette.database.models import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PaParauapebasSpider(BaseGazetteSpider):
    TERRITORY_ID = "1505536"
    name = "pa_parauapebas"
    allowed_domains = ["parauapebas.pa.gov.br"]
    start_urls = ["http://apps.ioepa.com.br/Parauapebas/Busca"]
    start_date = dt.date(2022, 1, 4)

    def parse(self, response):
        month = 1
        year = 2022
        for day in range(4, 30):
            data = f"{year}-{month}-{day}"
            url = f"https://apps.ioepa.com.br/Parauapebas/Busca?data={data}"
            yield scrapy.Request(
                url,
                callback=self.parse_gazette,
                cb_kwargs={"data": data},
            )

    def parse_gazette(self, response, data):
        link_diario = response.css("a[target]").css("::attr(href)").extract_first()
        edition_number = 1
        yield Gazette(
            date=data,
            edition_number=edition_number,
            file_urls=[link_diario],
            is_extra_edition=False,
            power="executive",
        )
