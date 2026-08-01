import re
from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import yearly_sequence
from gazette.utils.extraction import get_date_from_text


class RjBarraMansaSpider(BaseGazetteSpider):
    TERRITORY_ID = "3300407"
    allowed_domains = ["barramansa.rj.gov.br"]
    name = "rj_barra_mansa"
    start_urls = ["https://portaltransparencia.barramansa.rj.gov.br/boletim-oficial/"]
    start_date = date(2017, 1, 3)

    def start_requests(self):
        for year in yearly_sequence(self.start_date, self.end_date):
            if year == datetime.today().year:
                yield Request(self.start_urls[0])
            else:
                yield Request(f"{self.start_urls[0]}?wpdmc=boletim-{year}")

    def parse(self, response):
        for element in response.css(".__dt_row"):
            gazette_info = element.css("td strong::text").get()

            date = get_date_from_text(re.search(r"de(.*)", gazette_info).group(1))

            edition_match = re.search(r"(\d+)", gazette_info)
            edition_number = edition_match.group(1) if edition_match else None
            # 2 janeiro 2020 is the only known extra edition case
            is_extra_edition = True if "extra" in gazette_info.lower() else False

            path_to_gazette = (
                element.css(".__dt_col_download_link a")
                .xpath("@data-downloadurl")
                .get()
            )

            if date is None or date > self.end_date:
                continue
            if date < self.start_date:
                return

            yield Gazette(
                date=date,
                file_urls=[path_to_gazette],
                is_extra_edition=is_extra_edition,
                power="executive",
                edition_number=edition_number,
            )
