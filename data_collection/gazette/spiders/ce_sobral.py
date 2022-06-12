import datetime as dt
import re

from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class CeSobralSpider(BaseGazetteSpider):
    name = "ce_sobral"
    TERRITORY_ID = "2312908"
    start_date = dt.date(2017, 2, 6)

    BASE_URL = "https://www.sobral.ce.gov.br/diario/pesquisa/index"

    def start_requests(self):
        months_by_year = [
            (date.month, date.year)
            for date in rrule(
                MONTHLY, dtstart=self.start_date.replace(day=1), until=self.end_date
            )
        ]
        for month, year in months_by_year:
            yield Request(
                url=f"{self.BASE_URL}/ano_da_publicacao:{year}/mes_da_publicacao:{month}",
                cb_kwargs={"month": month, "year": year},
            )

    def parse(self, response, month, year, page=1):
        gazette_results = response.xpath("//ul[@class = 'resultado-busca']//article")
        for gazette in gazette_results:
            title = gazette.xpath("./a/h5/text()").get()
            edition_number = re.search(r"Diário Oficial Nº (\d+)", title).group(1)
            is_extra_edition = "suplementar" in title.lower()
            link = response.urljoin(
                gazette.xpath("./a[contains(@href, '.pdf')]/@href").get()
            )
            gazette_content_sample = gazette.xpath(".//p/text()").get()
            raw_date = re.search(r"\d{2}/\d{2}/\d{4}", gazette_content_sample).group()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield Gazette(
                date=date,
                file_urls=[link],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        next_page = response.css("ul.pagination").xpath(
            "./li[.//text()='chevron_right']"
        )
        if next_page and "disabled" not in next_page.attrib["class"]:
            yield Request(
                url=f"{self.BASE_URL}/ano_da_publicacao:{year}/mes_da_publicacao:{month}/pg:{page + 1}",
                cb_kwargs={"month": month, "year": year, "page": page + 1},
            )
