from datetime import date, datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import yearly_sequence


class SpSaoSebastiaoSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550704"
    name = "sp_sao_sebastiao"
    allowed_domains = ["saosebastiao.sp.gov.br"]
    start_date = date(2017, 3, 15)

    BASE_URL = "https://www.saosebastiao.sp.gov.br/doem.asp"

    async def start(self):
        # The website lists the gazettes of a single year per page
        # (doem.asp?Ano=YYYY). Without the parameter, only the current
        # year is shown.
        for year in yearly_sequence(self.start_date, self.end_date):
            yield Request(f"{self.BASE_URL}?Ano={year}")

    def parse(self, response):
        for gazette in response.css("div.doem-card"):
            raw_date = gazette.css("p::text").re_first(r"\d{2}/\d{2}/\d{4}")
            gazette_date = datetime.strptime(raw_date, "%d/%m/%Y").date()

            if self.start_date <= gazette_date <= self.end_date:
                edition_number = gazette.css("h4::text").re_first(r"\d+")
                gazette_url = response.urljoin(
                    gazette.css("a.doem-btn::attr(href)").get()
                )

                yield Gazette(
                    date=gazette_date,
                    edition_number=edition_number,
                    is_extra_edition=False,
                    power="executive_legislative",
                    file_urls=[gazette_url],
                )
