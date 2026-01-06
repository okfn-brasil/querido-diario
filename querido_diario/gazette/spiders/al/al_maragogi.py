import re
from datetime import date
from urllib.parse import parse_qs

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.extraction import get_date_from_text


class AlMaragogiSpider(BaseGazetteSpider):
    name = "al_maragogi"
    TERRITORY_ID = "2704500"
    allowed_domains = ["diario.maragogi.al.gov.br"]
    start_date = date(2024, 4, 17)
    BASE_URL = "https://diario.maragogi.al.gov.br"

    def start_requests(self):
        yield FormRequest(
            url=f"{self.BASE_URL}/busca",
            formdata=self.__create_params(),
            method="GET",
        )

    def parse(self, response, current_page=1):
        publications = response.css("div.publicacao > div.box-publicacao")
        for publication in publications:
            title_element = publication.css("h4 a::text")
            extra_edition = "extra" in title_element.get().lower()
            edition_number = title_element.re_first(r"nº (\d+)/", re.IGNORECASE)

            date_raw = publication.css("div div div::text").getall()[1].strip()
            item_date = get_date_from_text(date_raw)

            file_id = publication.css("h4 > a::attr(href)").get().strip().split("/")[-1]
            url = f"{self.BASE_URL}/diario-oficial/versao-pdf/{file_id}"

            yield Gazette(
                date=item_date,
                edition_number=edition_number,
                is_extra_edition=extra_edition,
                file_urls=[url],
                power="executive",
            )

        if current_page > 1:
            return

        last_page = self.__get_total_pages(response)
        for page in range(2, last_page + 1):
            yield FormRequest(
                url=f"{self.BASE_URL}/busca",
                formdata={"page": str(page), **self.__create_params()},
                method="GET",
                cb_kwargs={"current_page": page},
            )

    def __create_params(self) -> dict:
        return {
            "BuscaSearch[data_inicio]": self.start_date.strftime("%Y-%m-%d"),
            "BuscaSearch[data_fim]": self.end_date.strftime("%Y-%m-%d"),
            "BuscaSearch[sort]": "data_new",
            "BuscaSearch[modulo]": "diario-oficial",
        }

    @staticmethod
    def __get_total_pages(response) -> int:
        query = response.css("div.publicacao ul > li.last > a::attr(href)").get()
        if not query:
            return 0

        params = parse_qs(query.split("?")[-1])
        return int(params.get("page", ["0"])[0])
