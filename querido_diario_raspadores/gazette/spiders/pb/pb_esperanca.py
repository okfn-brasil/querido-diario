import datetime
import re

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PbEsperancaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2506006"
    name = "pb_esperanca"
    allowed_domains = ["esperanca.pb.gov.br"]
    start_urls = ["https://www.esperanca.pb.gov.br/publicacoes/quinzenarios"]
    start_date = datetime.date(2018, 4, 4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.start_date, str):
            self.start_date = datetime.datetime.strptime(
                self.start_date, "%Y-%m-%d"
            ).date()

    def parse(self, response):
        items = response.css("li.list-group-item a.text-muted")
        for item in items:
            raw_date = item.css("h6 span::text").re_first(r"(\d{2}/\d{2}/\d{4})")
            if not raw_date:
                continue

            gazette_date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()

            if gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            full_title = " ".join(item.css("h6 *::text, h6::text").getall()).strip()
            edition_regex = (
                r"QUINZEN[ÁA]RIO\s+OFICIAL\s+DE\s+ESPERAN[ÇC]A,?" r"\s+N[ºo°]?\s*(\d+)"
            )
            edition_match = re.search(edition_regex, full_title, re.IGNORECASE)
            edition_number = edition_match.group(1) if edition_match else ""
            is_extra_edition = "EXTRA" in full_title.upper() or not edition_number

            subpage_url = item.css("::attr(href)").get()
            yield response.follow(
                subpage_url,
                callback=self.parse_gazette,
                cb_kwargs={
                    "gazette_date": gazette_date,
                    "edition_number": edition_number,
                    "is_extra_edition": is_extra_edition,
                },
            )

        next_page_url = response.css("a[rel='next']::attr(href)").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_gazette(self, response, gazette_date, edition_number, is_extra_edition):
        file_urls = response.css("a[href$='.pdf']::attr(href)").getall()
        if not file_urls:
            css_selector = (
                "a[href*='/storage/content/publicacoes/quinzenarios/']" "::attr(href)"
            )
            file_urls = response.css(css_selector).getall()

        if file_urls:
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[response.urljoin(url) for url in file_urls],
                is_extra_edition=is_extra_edition,
                power="executive",
            )
