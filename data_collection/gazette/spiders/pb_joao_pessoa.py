import datetime
from urllib.parse import urlencode

import scrapy
from dateutil.rrule import MONTHLY, rrule

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbJoaoPessoaSpider(BaseGazetteSpider):
    name = "pb_joao_pessoa"
    TERRITORY_ID = "2507507"

    start_date = datetime.date(1992, 1, 1)

    def start_requests(self):
        base_url = "http://antigo.joaopessoa.pb.gov.br/semanariooficial/"
        url_params = {
            "querysearch": "1",
            "semanario_edicao": "-1",
            "submitsearch": "OK",
            "keyword": "",
        }
        initial_date = datetime.date(self.start_date.year, self.start_date.month, 1)
        end_date = datetime.date.today()

        periods_of_interest = [
            (date.year, date.month)
            for date in rrule(freq=MONTHLY, dtstart=initial_date, until=end_date)
        ]
        for year, month in periods_of_interest:
            url_params["semanario_ano"] = str(year)
            url_params["semanario_mes"] = str(month).zfill(2)

            parsed_params = urlencode(url_params)
            url = f"{base_url}?{parsed_params}"
            yield scrapy.Request(url=url)

    def parse(self, response):
        """Parses gazettes page and requests next page.

        Normal gazettes are displayed in a weekly basis, so, the date which is taken
        into account for this type of gazette is the last in the publication period
        (i.e. "29/08/2020" from "23/08/2020 to 29/08/2020").

        Special gazzetes are daily, but that same logic applies here and it works
        correctly.
        """
        gazettes = response.css(".table-semanarios table tbody tr")
        for gazette in gazettes:
            url = gazette.css("td:last-child a::attr(href)").get()
            gazette_date = (
                gazette.css("td:nth-last-child(2)::text")
                .re(r"[0-9]{2}/[0-9]{2}/[0-9]{4}")
                .pop()
            )
            gazette_date = datetime.datetime.strptime(gazette_date, "%d/%m/%Y").date()
            is_extra = "Especial" in gazette.css("td:first-child").get()

            yield Gazette(
                date=gazette_date,
                file_urls=[url],
                is_extra_edition=is_extra,
                power="executive_legislative",
            )

        for url in response.css(".pagination a.next::attr(href)").getall():
            yield response.follow(url)
