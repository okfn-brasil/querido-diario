import re

import dateparser
from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseAtendeV2Spider(BaseGazetteSpider):
    """
    Base spider for Gazettes that are available from cities listed on
    https://{city_subdomain}.atende.net
    This base class deals with 'Layout 2' gazette pages, usually requested
    from 'https://{city_subdomain}.atende.net/diariooficial'.
    """

    allowed_domains = ["atende.net"]
    BASE_URL = ""

    # Must be defined into child classes
    city_subdomain = ""

    def start_requests(self):
        self.BASE_URL = f"https://{self.city_subdomain}.atende.net/diariooficial/edicao/pagina/atende.php"

        yield FormRequest(
            url=self.BASE_URL,
            method="GET",
            formdata=self.get_params("pagina", 1),
            cb_kwargs={"page": 1},
        )

    def parse(self, response, page):
        for item in response.css("div.nova_listagem div.linha"):
            date_raw = item.css("div.data::text").get()
            date = dateparser.parse(date_raw, languages=["pt"]).date()

            if date > self.end_date:
                continue
            if date < self.start_date:
                return

            edition_type = item.css("div.tipo::text").get()
            is_extra = bool(
                re.search(
                    r"suplementar | retificação | extraordinária | extra",
                    edition_type,
                    re.IGNORECASE,
                )
            )

            edition_number = item.css("div.titulo::text").re_first(r"\d+")
            download_url = item.css("button::attr(data-link)")[-1].get()

            yield Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra,
                file_urls=[download_url],
                power="executive_legislative",
            )

        if page < self.get_last_page(response):
            yield FormRequest(
                url=self.BASE_URL,
                method="GET",
                formdata=self.get_params("pagina", page + 1),
                cb_kwargs={"page": page + 1},
            )

    def get_params(self, filtro, value):
        params = {
            "rot": "54015",
            "aca": "101",
            "ajax": "t",
            "processo": "loadPluginDiarioOficial",
        }
        if filtro == "pagina":
            params[
                "parametro"
            ] = f'{{"codigoPlugin":1,"filtroPlugin":{{"pagina":"{value}"}}}}'
        elif filtro == "edicao":
            params[
                "parametro"
            ] = f'{{"codigoPlugin":2,"filtroPlugin":{{"codigoEdicao":"{value}"}}}}'

        return params

    def get_last_page(self, response):
        pages = response.css("div#paginacao li.dst button::attr(value)").getall()[-1]
        return int(pages)
