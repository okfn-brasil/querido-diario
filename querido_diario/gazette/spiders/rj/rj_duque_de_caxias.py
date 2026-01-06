import re
from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import yearly_sequence
from gazette.utils.extraction import get_date_from_text


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    name = "rj_duque_de_caxias"
    TERRITORY_ID = "3301702"
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    start_date = date(2017, 1, 2)

    def start_requests(self):
        current_year = datetime.today().year
        for year in yearly_sequence(self.start_date, self.end_date):
            if year == current_year:
                yield Request(
                    "https://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"
                )
            else:
                yield Request(f"https://duquedecaxias.rj.gov.br/portal/{year}.html")

    def parse(self, response):
        pdf_divs = response.xpath(
            "//i[contains(@class, 'fa-file-pdf')]/ancestor::div[1]"
        )
        # use descending order to reduce iterations in the daily crawl
        for pdf_div in pdf_divs[::-1]:
            raw_gazette_date = pdf_div.xpath("./preceding-sibling::div[1]/text()").get()
            gazette_date = get_date_from_text(raw_gazette_date)
            if not gazette_date or gazette_date > self.end_date:
                continue
            if gazette_date < self.start_date:
                return

            raw_gazette_edtion = pdf_div.xpath("./preceding-sibling::div[2]/text()")
            is_extra_edition = bool(
                re.search(r"extra|esp", raw_gazette_edtion.get(), re.IGNORECASE)
            )
            edition_number = (
                None if is_extra_edition else raw_gazette_edtion.re_first(r"\d+")
            )

            gazette_url = response.urljoin(pdf_div.xpath(".//a/@href").get())

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                file_urls=[gazette_url],
                power="executive_legislative",
            )
