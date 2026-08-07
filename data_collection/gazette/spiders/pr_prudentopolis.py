import datetime

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrPrudentopolisSpider(BaseGazetteSpider):
    TERRITORY_ID = "4120606"
    name = "pr_prudentopolis"
    start_date = datetime.date(2010, 5, 27)
    start_urls = ["https://www.prudentopolis.pr.gov.br/diario-oficial/"]
    base_file_url = "https://www.prudentopolis.pr.gov.br"
    current_page = 1
    custom_settings = {"DOWNLOAD_DELAY": 2.0, "CONCURRENT_REQUESTS": 10}

    def parse(self, response):
        file_metadata = {}
        page_prefix = response.xpath(
            '//ul[contains(@class, "pagination")]/li/a/@href'
        ).get()[:-1]

        next_page = f"{page_prefix}{self.current_page}"
        self.current_page += 1
        current_url = f"{self.start_urls[0]}{next_page}"

        table = response.xpath('//table[@id="listagem-itens"]//tbody')

        if not table:
            return

        for row in table.xpath("//tr"):
            date = row.xpath("td[2]/text()").get()
            if date is not None:
                date = datetime.datetime.strptime(
                    date.replace(" ", "").replace("\n", ""), "%d/%m/%Y"
                ).date()
                file_url = row.xpath("td[3]/a/@href").get().replace(" ", "")
                file_metadata[date] = file_url

        dates_to_parse = filter(
            lambda x: self.start_date <= x <= self.end_date, list(file_metadata.keys())
        )

        for date in dates_to_parse:
            url = f"{self.base_file_url}{file_metadata[date]}"

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                territory_id=self.TERRITORY_ID,
                power="executive_legislative",
                scraped_at=datetime.datetime.utcnow(),
            )

        if min(file_metadata.keys()) < self.start_date:
            return

        yield Request(current_url, dont_filter=True)
