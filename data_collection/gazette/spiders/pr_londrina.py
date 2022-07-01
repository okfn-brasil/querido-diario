import datetime as dt
import re

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrLondrina(BaseGazetteSpider):
    TERRITORY_ID = "4113700"
    name = "pr_londrina"
    allowed_domains = ["londrina.pr.gov.br"]
    start_urls = ["https://www2.londrina.pr.gov.br/jornaloficial/"]
    start_date = dt.date(1997, 2, 6)

    def parse(self, response, current_page=1):
        rows = response.css("table.adminlist").xpath(".//tr[contains(@class, 'row')]")

        for row in rows:
            href = row.css("a::attr(href)").get()
            url = response.urljoin(href)
            edition_number = (
                re.search(r"/jornal[\w ]*?(\d+)", url, re.IGNORECASE)
                .group(1)
                .lstrip("0")
            )
            title = row.css("a::text").get()
            is_extra_edition = "extra" in title.lower()
            raw_date = row.xpath("./td[2]/text()").get().strip()
            date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
            # parse(date, languages=["pt"]).date()

            if date > self.end_date:
                continue
            elif date < self.start_date:
                return

            yield Gazette(
                date=date,
                file_urls=[url],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        pagination = response.xpath("//input[@value='>>']")
        if not pagination:
            return

        yield FormRequest(
            response.url,
            formdata={"hpage": str(current_page + 1)},
            cb_kwargs={"current_page": current_page + 1},
        )
