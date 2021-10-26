import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbSantaRitaSpiderExecutive(BaseGazetteSpider):
    TERRITORY_ID = "2513703"
    allowed_domains = ["santarita.pb.gov.br"]
    name = "pb_santa_rita"
    start_urls = ["https://www.santarita.pb.gov.br/diario-oficial/diario-oficial-2021/"]

    def parse(self, response):
        # handle current year
        yield from self.parse_year(response)

        # handle remaining years
        years_urls = response.css(".current-menu-item ~ li a::attr(href)").getall()
        yield from response.follow_all(years_urls, self.parse_year)

    def parse_year(self, response):
        for edition in response.css(".columnRight .card"):
            title = edition.css(".infoTitle a::text")

            yield Gazette(
                edition_number=title.re_first(r"n\. (\d+)"),
                date=dateparser.parse(edition.css(".infoDate::text").get()).date(),
                file_urls=[edition.css("a.downloadEnabled::attr(href)").get()],
                is_extra_edition=bool(title.re_first(r"(?i)\bextra\b")),
                power="executive",
            )

        if next_page := response.css(".sogocdn-pagination .next::attr(href)").get():
            yield response.follow(next_page, callback=self.parse_year)
