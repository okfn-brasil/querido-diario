import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SaiGazetteSpider(BaseGazetteSpider):
    """
    Base Spider for all cases with use SAI (Serviço de Acesso a Informação)
    Read more in https://imap.org.br/sistemas/sai/

    Attributes
    ----------
    base_url : str
        It must be defined in child classes.
        If the domain is sai.io.org.br you must add the subpat otherwise use the domain only
        e.g:
            - sai domain: https://sai.io.org.br/ba/maragojipe
            - other domain: https://www.igaci.al.gov.br/site/diariooficial

    start_date : datetime.date
        Must be get into execution from website
    """

    base_url = None
    start_date = None

    @property
    def _site_url(self):
        return f"{self.base_url}/Site/DiarioOficial"

    def start_requests(self):
        yield scrapy.Request(url=self._site_url, callback=self._pagination_requests)

    def _pagination_requests(self, response):
        client_id = response.xpath(
            "//select[@id='cod_cliente']/option[2]/@value"
        ).extract_first()

        if not self.start_date:
            first_year = int(
                response.xpath("//select[@id='ano']/option[last()]/@value")
                .extract_first()
                .strip()
            )
            self.start_date = dt.date(first_year, 1, 1)

        for year in range(self.start_date.year, self.end_date.year + 1):
            formdata = {
                "URL": "/Site/GetSubGrupoDiarioOficial",
                "diarioOficial.cod_cliente": f"{client_id}",
                "diarioOficial.tipoFormato": "1",
                "diarioOficial.ano": f"{year}",
                "diarioOficial.dataInicial": self.start_date.strftime("%Y-%m-%d"),
                "diarioOficial.dataFinal": self.end_date.strftime("%Y-%m-%d"),
            }

            yield scrapy.FormRequest(
                url=self._site_url,
                formdata=formdata,
                callback=self.parse_item,
                cb_kwargs={"client_id": client_id},
            )

    def parse_item(self, response, client_id):
        gazette_list = response.json()
        for gazette_item in gazette_list:
            edition_number = gazette_item["cod_documento"]
            date = dt.datetime.fromisoformat(gazette_item["dat_criacao"]).date()
            file_url = f"https://sai.io.org.br/Handler.ashx?f=diario&query={edition_number}&c={client_id}&m=0"
            yield Gazette(
                date=date,
                file_urls=[file_url],
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
            )
