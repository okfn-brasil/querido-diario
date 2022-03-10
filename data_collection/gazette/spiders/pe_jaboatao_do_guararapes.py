from datetime import date

import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeJaboataoDosGuararapesSpiderExecutive(BaseGazetteSpider):
    TERRITORY_ID = "2607901"
    allowed_domains = ["jaboatao.pe.gov.br"]
    name = "pe_jaboatao_dos_guararapes"
    start_urls = ["https://diariooficial.jaboatao.pe.gov.br/"]
    start_date = date(2015, 10, 3)
    end_date = date.today()

    def parse(self, response):
        for edition in response.css(".post"):
            gazette_date = dateparser.parse(
                edition.css(".elementor-post-date::text").get()
            ).date()

            if gazette_date < self.start_date:
                return
            elif gazette_date > self.end_date:
                continue
            else:
                yield Gazette(
                    date=gazette_date,
                    file_urls=[edition.css("a::attr(href)").get()],
                    is_extra_edition="extra" in edition.css("a::text").get().lower(),
                    power="executive",
                )

        next_page = response.css(".elementor-pagination .next::attr(href)").get()
        if next_page:
            yield response.follow(next_page)
