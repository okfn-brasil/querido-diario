from datetime import date

from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaImperatrizSpider(BaseGazetteSpider):
    name = "ma_imperatriz"

    start_urls = ["http://www.diariooficial.imperatriz.ma.gov.br/edicoes"]
    start_date = date(2021, 4, 19)
    TERRITORY_ID = "2105302"

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": "http://www.diariooficial.imperatriz.ma.gov.br/edicoes",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        },
    }

    def parse(self, response):
        for issue in response.css(".deprt-icon-box"):
            gazette_date = parse(
                issue.css("h6").re_first(r"(\d+/\d+/\d+)"),
                languages=["pt"],
            ).date()

            if gazette_date < self.start_date:
                return
            if gazette_date > self.end_date:
                continue

            yield Gazette(
                date=gazette_date,
                edition_number=issue.css("h6").re_first(r"Nº (\d+/\d+)"),
                file_urls=[issue.css("a::attr(href)").get()],
                is_extra_edition=False,
                power="executive",
            )

        for next_page in response.css(".page-link[rel=next]::attr(href)"):
            yield response.follow(next_page.get())
