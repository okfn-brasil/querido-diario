import datetime as dt
from urllib.parse import urlencode

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToSampaioSpider(BaseGazetteSpider):
    TERRITORY_ID = "1718808"
    name = "to_sampaio"
    allowed_domains = ["sampaio.to.gov.br"]
    start_date = dt.date(2020, 5, 4)

    def get_url(self, page=1):
        url_params = {
            "pagina": page,
            "data_inicial": self.start_date.strftime("%d/%m/%Y"),
            "data_final": self.end_date.strftime("%d/%m/%Y"),
        }

        return (
            f"https://diariooficial.sampaio.to.gov.br/pesquisar?{urlencode(url_params)}"
        )

    def start_requests(self):
        yield scrapy.Request(url=self.get_url())

    def parse(self, response, current_page=1):
        editions = response.css("#resultados tr.tr_table_list_loop")
        for edition in editions:
            raw_date = edition.xpath("./td[3]/text()").get()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

            gazette_url = edition.css("a::attr(href)").get()
            title = edition.xpath("./td[1]/a/div//text()")
            is_extra_edition = "extra" in " ".join(title.getall()).lower()
            edition_number = title.re_first(r"\d+")
            yield Gazette(
                date=date,
                file_urls=[gazette_url],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        pagination = response.css("#paginacao_area a:contains('Próxima')").get()
        if pagination:
            next_page = current_page + 1
            yield scrapy.Request(
                url=self.get_url(page=next_page),
                cb_kwargs={"current_page": next_page},
            )
