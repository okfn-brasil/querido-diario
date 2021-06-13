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
                url=f"http://www.sobral.ce.gov.br/diario/pesquisa/index/ano_da_publicacao:{search_month.year}/mes_da_publicacao:{search_month.month}/#resultado",
                callback=self.parse_gazettes,
                meta={"search_month": search_month},
            )

    def parse_gazettes(self, response):
        search_month = response.meta.get("search_month")
        total_gazettes = response.xpath("//div[@class = 'right']/text()").get()
        cur_page = response.xpath("//li[@class = 'active']/a/text()").get()
        done = 0
        if int(total_gazettes) > 0:
            gazette_results = response.xpath(
                "//ul[@class = 'resultado-busca']//article"
            )
            for gazette in gazette_results:
                link = response.urljoin(
                    gazette.xpath("./a[contains(@href, '.pdf')]/@href").get()
                )
                title = gazette.xpath("./a/h5/text()").get()
                edition_number = re.search(r"Diário Oficial Nº (\d+)", title).group(1)
                extra_edition = "Suplementar" in title
                gazette_content_sample = gazette.xpath(".//p/text()").get()
                date = dateparser.parse(
                    re.search(r"^\d{2}/\d{2}/\d{4}", gazette_content_sample).group(0),
                    date_formats=["%d/%m/%Y"],
                ).date()
                if date >= self.start_date:
                    yield Gazette(
                        date=date,
                        file_urls=[link],
                        edition_number=edition_number,
                        is_extra_edition=extra_edition,
                        power="executive_legislative",
                    )
                else:
                    done = 1

            if (done == 0) & (cur_page is not None):
                next_page = int(cur_page) + 1
                if (
                    response.xpath(
                        f"//li[@class = 'waves-effect']/a[contains(text(), {next_page})]"
                    )
                    is not None
                ):
                    yield Request(
                        url=f"http://www.sobral.ce.gov.br/diario/pesquisa/index/ano_da_publicacao:{search_month.year}/mes_da_publicacao:{search_month.month}/pg:{next_page}/#resultado",
                        callback=self.parse_gazettes,
                        meta={"search_month": search_month},
                    )
