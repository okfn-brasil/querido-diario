import datetime

from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrPrudentopolis(BaseGazetteSpider):
    TERRITORY_ID = "4120606"
    name = "pr_prudentopolis"
    start_date = datetime.date(2010, 5, 27)
    allowed_domains = ["prudentopolis.pr.gov.br", "l2fsistemasweb.com.br"]
    start_urls = ["https://www.prudentopolis.pr.gov.br/diario-oficial/"]

    def parse(self, response):
        start_url = "https://www.prudentopolis.pr.gov.br/diario-oficial/"
        download_url = "https://www.prudentopolis.pr.gov.br"

        lines = response.xpath("//tbody/tr")

        urls = []
        for relative_url in lines:
            url = relative_url.xpath("td[4]/a/@href").extract()[0]
            if "l2fsistemasweb.com.br" not in url:
                url = url.replace(" ", "")
                urls.append(f"{download_url}{url}")
            else:
                urls.append(url.replace(" ", ""))

        dates = [
            parse(date, languages=["pt"]).date()
            for date in lines.xpath("td[2]/text()").extract()
        ]

        for url, date in zip(urls, dates):
            yield Gazette(
                date=date,
                file_urls=[url],
                power="executive_legislative",
            )

        final_page = response.xpath(
            '//ul[contains(@class, "pagination pagination-centered")]/li/a/@href'
        )[-2].extract()
        number_final_page = int(final_page[-2:])

        for page in range(2, number_final_page + 1):
            yield response.follow(f"{start_url}{final_page[:-2]}{page}")
