import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AmManausSpider(BaseGazetteSpider):
    name = "ma_timon"
    start_date = datetime.date(2013, 3, 20)
    start_urls = ["https://timon.ma.gov.br/diario/pesquisa.php"]

    TERRITORY_ID = "2112209"

    def start_requests(self) -> scrapy.FormRequest:
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")
        base_url = "https://timon.ma.gov.br/diario/pesquisa.php"

        params = {
            "TipoDiario_datas": "Executivo",  # (Legislativo, Executivo, Todos)
            "editData_inicio": start_date,
            "editData_fim": end_date,
        }

        yield scrapy.FormRequest(
            url=base_url,
            method="POST",
            formdata=params,
            callback=self.parse,
            # cb_kwargs={"params": params},
        )

    def parse(self, response) -> Gazette:
        trs = response.xpath(
            "/html/body/div/header/div[2]/header/div/div[1]/header/div[2]/div/div/table/tbody/tr"
        )
        for tr in trs:
            # import pdb; pdb.set_trace()
            edition_number = tr.xpath("td[2]/text()")[0].get()
            gazette_date = datetime.datetime.strptime(
                tr.xpath("td[3]/text()")[0].get(), "%d/%m/%Y"
            ).date()
            gazette_url = tr.xpath("td[6]/a/@href").get()
            is_extra = tr.xpath("td[5]/text()")[0].get() == "SUPLEMENTAR"

            if gazette_date is not None and (
                gazette_date < self.start_date or gazette_date > self.end_date
            ):
                continue

            yield Gazette(
                date=gazette_date,
                file_urls=[gazette_url],
                edition_number=edition_number,
                is_extra_edition=is_extra,
                power="executive",
            )
