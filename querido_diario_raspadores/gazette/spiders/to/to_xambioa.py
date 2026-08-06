from datetime import date

from scrapy import Request
from w3lib.url import add_or_replace_parameter

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToXambioaSpider(BaseGazetteSpider):
    TERRITORY_ID = "1722107"
    name = "to_xambioa"
    allowed_domains = ["diariooficial.xambioa.to.gov.br"]
    start_date = date(2021, 5, 24)
    base_url = "https://diariooficial.xambioa.to.gov.br/api/diarios"

    async def start(self):
        url = f"{self.base_url}?calendar=true&situacao=2&per_page=100&page=1"
        yield Request(url)

    def parse(self, response):
        response_data = response.json()

        for edition in response_data["data"]:
            edition_date = date.fromisoformat(edition["data"])
            if not self.start_date <= edition_date <= self.end_date:
                continue

            file_url = edition["media_legacy"] or edition["midias"][0]["url"]
            edition_type = edition["tipo"]["descricao"]

            yield Gazette(
                date=edition_date,
                edition_number=edition["numero"],
                file_urls=[file_url],
                is_extra_edition=edition_type == "Edição Especial",
                power="executive_legislative",
            )

        current_page = response_data["current_page"]
        if current_page < response_data["last_page"]:
            next_page_url = add_or_replace_parameter(
                response.url, "page", current_page + 1
            )
            yield Request(next_page_url)
