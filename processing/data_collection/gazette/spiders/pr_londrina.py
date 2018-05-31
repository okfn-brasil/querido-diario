from dateparser import parse
import datetime as dt

from scrapy import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrLondrina(BaseGazetteSpider):
    MUNICIPALITY_ID = '4113700'
    name = 'pr_londrina'
    allowed_domains = ['londrina.pr.gov.br']
    start_urls = ['http://www2.londrina.pr.gov.br/jornaloficial/']

    def parse(self, response):
        """
        @url http://www2.londrina.pr.gov.br/jornaloficial/
        @returns items 20
        """
        lines = response.xpath('//table[contains(@class, "adminlist")]/tr')

        urls = [response.urljoin(relative_url)
                for relative_url in lines.xpath('td[1]/a/@href').extract()]
        is_extra_edition = ['Extra' in text
                            for text in lines.xpath('td[1]/a/text()').extract()]
        dates = [parse(date, languages=['pt']).date()
                 for date in lines.xpath('td[2]/text()').extract()]

        for url, is_extra, date in zip(urls, is_extra_edition, dates):
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive_legislature',
                scraped_at=dt.datetime.utcnow(),
            )

        for page in range(2, len(response.css('.button.othersOptPage')) + 1):
            yield FormRequest(response.url, formdata={'hpage': str(page)}, callback=self.parse)
