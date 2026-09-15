import datetime as dt

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PaParauapebasSpider(BaseGazetteSpider):
    TERRITORY_ID = "1505536"
    name = "pa_parauapebas"
    start_urls = ["http://apps.ioepa.com.br/Parauapebas/Busca"]
    start_date = dt.date(2022, 1, 4)

    def parse(self, response):
        ano_atual = dt.datetime.now().year
        for year in [2022, ano_atual]:
            for month in range(1, 13):
                for day in range(1, 32):
                    if len(str(day)) < 2:
                        day = "".join(("0", str(day)))
                    if len(str(month)) < 2:
                        month = "".join(("0", str(month)))
                    data = f"{year}-{month}-{day}"
                    url = f"{response.url}?data={data}"
                    yield scrapy.Request(
                        url,
                        callback=self.parse_gazette,
                        cb_kwargs={"data": data},
                    )

    def parse_gazette(self, response, data):
        link_diario = response.css("a[target]").css("::attr(href)").extract_first()
        data_do_diario = link_diario.split("/")[-1].split(".")[:-2]
        data_no_formato_string = str(data)
        data = data_no_formato_string.split("-")
        if data_do_diario == data:
            data_no_formato_date = parse(
                data_no_formato_string, languages=["br"]
            ).date()
            yield Gazette(
                date=data_no_formato_date,
                file_urls=[link_diario],
                is_extra_edition=False,
                power="executive",
            )
