from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaPeritoroSpider(BaseGazetteSpider):
    TERRITORY_ID = "2108454"
    name = "ma_peritoro"
    allowed_domains = ["peritoro.ma.gov.br"]
    start_urls = ["https://dom.peritoro.ma.gov.br/"]
    start_date = date(2022, 4, 5)
    next_page = 1

    def parse(self, response):
        have_found_gazette = False

        for title in response.css("h4.elementor-post__title"):
            have_found_gazette = True
            edition_number = self._get_edition_number(title)
            gazette_date = self._get_date(edition_number)

            if self._should_get_gazette(gazette_date):
                yield Request(
                    title.css('a::attr("href")').get(),
                    callback=self._parse_title_page,
                    meta={
                        "edition_number": edition_number,
                        "gazette_date": gazette_date,
                    },
                )
            else:
                self.logger.info(
                    f"Ignoring gazette with {gazette_date} for not in defined "
                    f"range [start: {self.start_date} - end: {self.end_date}]"
                )
                continue

        if have_found_gazette:
            self.next_page += 1
            yield Request(f"{self.start_urls[0]}page/{self.next_page}/")

    def _get_edition_number(self, title):
        raw_edition = title.css("a::text").get()

        return raw_edition.replace("\t", "").replace("\n", "")

    def _get_date(self, edition_number):
        date_only = edition_number.replace("DOM", "")

        return datetime.strptime(date_only, "%Y%m%d").date()

    def _should_get_gazette(self, gazette_date):
        if self.end_date is not None:
            return self.start_date <= gazette_date <= self.end_date

        return gazette_date >= self.start_date

    def _parse_title_page(self, response):
        gazette_url = (
            response.css("a.wp-block-file__button.wp-element-button")
            .css('a::attr("href")')
            .get()
        )

        if not gazette_url:
            self.logger.info(f"No document found on < {response.url} >")
            return

        yield Gazette(
            date=response.meta["gazette_date"],
            edition_number=response.meta["edition_number"],
            file_urls=[gazette_url],
            power="executive",
            is_extra_edition=False,
        )
