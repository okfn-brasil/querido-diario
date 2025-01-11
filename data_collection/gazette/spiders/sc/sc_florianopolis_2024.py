from datetime import date, datetime

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ScFlorianopolisSpider(BaseGazetteSpider):
    name = "sc_florianopolis_2024"
    TERRITORY_ID = "4205407"
    start_date = date(2024, 8, 5)
    allowed_domains = ["edicao.dom.sc.gov.br"]

    def _requests(self, page):
        formdata = {
            "Edicao[cod_municipio]": "146",
            "Edicao_page": str(page),
            "r": "site/edicoes",
        }
        return FormRequest(
            url="https://edicao.dom.sc.gov.br/?",
            method="GET",
            formdata=formdata,
            callback=self.parse_pagination,
            cb_kwargs={"page": page},
        )

    def start_requests(self):
        yield self._requests(1)

    def parse_pagination(self, response, page):
        for item in response.css("tbody tr"):
            edition_number = item.css("td::text")[1].get()
            edition_url = item.css("td a")[1].attrib["href"]
            raw_date = item.css("td::text")[2].get()
            edition_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            if self.start_date <= edition_date <= self.end_date:
                yield Gazette(
                    date=edition_date,
                    edition_number=edition_number,
                    is_extra_edition=False,
                    power="executive_legislative",
                    file_urls=[edition_url],
                )

        if edition_date > self.start_date:
            yield self._requests(page + 1)
