import datetime as dt

from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class CeSobralSpider(BaseGazetteSpider):
    name = "ce_sobral"
    TERRITORY_ID = "2312908"
    start_date = dt.date(1998, 6, 10)

    BASE_URL = "https://www.sobral.ce.gov.br/diario/pesquisa/index"

    def start_requests(self):
        if self.start_date < dt.date(2017, 2, 3):
            # Gazettes older than 03/02/2017 are available at
            # https://www.sobral.ce.gov.br/diario/iom
            yield Request("https://www.sobral.ce.gov.br/diario/iom", self.parse_older)

        if self.end_date > dt.date(2017, 2, 3):
            start_date = max([self.start_date, dt.date(2017, 2, 3)])

            months_by_year = [
                (date.month, date.year)
                for date in rrule(
                    MONTHLY, dtstart=start_date.replace(day=1), until=self.end_date
                )
            ]
            for month, year in months_by_year:
                yield Request(
                    url=f"{self.BASE_URL}/ano_da_publicacao:{year}/mes_da_publicacao:{month}",
                    cb_kwargs={"month": month, "year": year},
                )

    def parse_older(self, response):
        """Parse gazettes with publish date older than 03/02/2017"""
        gazettes = response.xpath("//a[contains(@href, 'pdf')]//ancestor::td[1]")
        for gazette in gazettes:
            gazette_raw_date = gazette.xpath(".//following-sibling::td[1]").re_first(
                r"\d{2}/\d{2}/\d{4}", ""
            )
            gazette_date = dt.datetime.strptime(gazette_raw_date, "%d/%m/%Y").date()
            if gazette_date > self.end_date:
                continue
            elif gazette_date < self.start_date:
                continue

            gazette_url = gazette.css("a::attr(href)").get()
            gazette_description = gazette.css("::text")
            edition_number = gazette_description.re_first(r"(\d+)")
            is_extra_edition = "extra" in "".join(gazette_description.getall()).lower()

            yield Gazette(
                date=gazette_date,
                file_urls=[
                    gazette_url,
                ],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

    def parse(self, response, month, year, page=1):
        gazettes = response.css(".resultado-busca article")
        for gazette in gazettes:
            title = gazette.css("h5::text")
            edition_number = title.re_first(r"Diário Oficial Nº (\d+)")
            is_extra_edition = "suplementar" in title.get().lower()

            link = response.urljoin(
                gazette.xpath("./a[contains(@href, '.pdf')]/@href").get()
            )
            gazette_raw_date = gazette.css("p::text").re_first(r"\d{2}/\d{2}/\d{4}", "")
            gazette_date = dt.datetime.strptime(gazette_raw_date, "%d/%m/%Y").date()

            if gazette_date > self.end_date:
                continue
            elif gazette_date < self.start_date:
                return

            yield Gazette(
                date=gazette_date,
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
