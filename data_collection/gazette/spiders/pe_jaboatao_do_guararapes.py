import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeJaboataoDosGuararapesSpiderExecutive(BaseGazetteSpider):
    TERRITORY_ID = "3304904"
    allowed_domains = ["jaboatao.pe.gov.br"]
    name = "pe_jaboatao_dos_guararapes"
    start_urls = ["https://diariooficial.jaboatao.pe.gov.br/"]

    def parse(self, response):
        for edition in response.css(".post"):
            yield Gazette(
                date=dateparser.parse(
                    edition.css(".elementor-post-date::text").get()
                ).date(),
                file_urls=[edition.css("a::attr(href)").get()],
                is_extra_edition="extra" in edition.css("a::text").get().lower(),
                power="executive",
            )

        if next_page := response.css(".elementor-pagination .next::attr(href)").get():
            yield response.follow(next_page)
