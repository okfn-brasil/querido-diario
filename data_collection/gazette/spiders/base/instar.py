import datetime
import math

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaseInstarSpider(BaseGazetteSpider):
    def start_requests(self):
        page = 1
        start_date = self.start_date.strftime("%d-%m-%Y")
        end_date = self.end_date.strftime("%d-%m-%Y")

        start_url = f"{self.base_url}/{page}/{start_date}/{end_date}/0/0/"

        yield scrapy.Request(
            start_url,
            cb_kwargs={"page": page, "start_date": start_date, "end_date": end_date},
        )

    def _pagination_requests(self, response, page, start_date, end_date):
        if page == 1:
            num_results = int(response.css(".sw_qtde_resultados::text").get("0"))
            results_per_page = 50
            total_pages = math.ceil(num_results / results_per_page)

            for next_page in range(2, total_pages + 1):
                next_page_url = (
                    f"{self.base_url}/{next_page}/{start_date}/{end_date}/0/0/"
                )

                yield scrapy.Request(
                    next_page_url,
                    cb_kwargs={
                        "page": next_page,
                        "start_date": start_date,
                        "end_date": end_date,
                    },
                )

    def parse(self, response, page, start_date, end_date):
        gazettes = response.css(".dof_publicacao_diario")
        for gazette in gazettes:
            raw_gazette_date = gazette.css("span::text").re_first(
                r"\d{2}\/\d{2}\/\d{4}"
            )
            gazette_date = datetime.datetime.strptime(
                raw_gazette_date, "%d/%m/%Y"
            ).date()
            edition_number = gazette.css(".dof_titulo_publicacao span::text").re_first(
                r"\d+"
            )
            gazette_url = response.urljoin(gazette.css("a::attr(href)").get())

            item = Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=False,
                power="executive_legislative",
            )

            yield scrapy.Request(
                gazette_url, callback=self.parse_gazette_url, cb_kwargs={"item": item}
            )

        yield from self._pagination_requests(response, page, start_date, end_date)

    def parse_gazette_url(self, response, item):
        gazette_url = response.urljoin(
            response.css(".d_titulo_edicao a::attr(href)").get()
        )
        yield Gazette(
            file_urls=[
                gazette_url,
            ],
            **item,
        )
