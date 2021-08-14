import re
from datetime import date

import dateparser
from dateutil.rrule import MONTHLY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class CeSobralSpider(BaseGazetteSpider):
    name = "ce_sobral"
    TERRITORY_ID = "2312908"
    start_date = date(2017, 2, 6)
    end_date = date.today()

    def start_requests(self):
        for search_month in rrule(
            MONTHLY, dtstart=self.start_date.replace(day=1), until=self.end_date
        ):
            yield Request(
                url=f"https://www.sobral.ce.gov.br/diario/pesquisa/index/ano_da_publicacao:{search_month.year}/mes_da_publicacao:{search_month.month}",
                callback=self.parse_gazettes,
                meta={"search_month": search_month},
            )

    def parse_gazettes(self, response):
        total_gazettes = response.xpath("//div[@class = 'right']/text()").get()
        if int(total_gazettes) == 0:
            return

        gazette_results = response.xpath("//ul[@class = 'resultado-busca']//article")
        for gazette in gazette_results:

            # Extract attributes
            title = gazette.xpath("./a/h5/text()").get()
            edition_number = re.search(r"Diário Oficial Nº (\d+)", title).group(1)
            extra_edition = "Suplementar" in title
            link = response.urljoin(
                gazette.xpath("./a[contains(@href, '.pdf')]/@href").get()
            )
            gazette_content_sample = gazette.xpath(".//p/text()").get()
            date = dateparser.parse(
                re.search(r"^\d{2}/\d{2}/\d{4}", gazette_content_sample).group(0),
                date_formats=["%d/%m/%Y"],
            ).date()
            yield Gazette(
                date=date,
                file_urls=[link],
                edition_number=edition_number,
                is_extra_edition=extra_edition,
                power="executive_legislative",
            )

            # Go to next page
            current_page = response.xpath("//li[@class = 'active']/a/text()").get()
            if current_page:
                next_page = int(current_page) + 1
                if response.xpath(
                    f"//li[@class = 'waves-effect']/a[contains(text(), {next_page})]"
                ):
                    search_month = response.meta.get("search_month")
                    yield Request(
                        url=f"https://www.sobral.ce.gov.br/diario/pesquisa/index/ano_da_publicacao:{search_month.year}/mes_da_publicacao:{search_month.month}/pg:{next_page}",
                        callback=self.parse_gazettes,
                        meta={"search_month": search_month},
                    )
