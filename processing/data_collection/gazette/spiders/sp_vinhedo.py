from datetime import date, datetime
import re

from dateparser import parse
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpVinhedoSpider(BaseGazetteSpider):

    # define class variables
    allowed_domains = ['vinhedo.sp.gov.br']
    name = 'sp_vinhedo'
    start_urls = [
        'http://vinhedo.sp.gov.br/arquivos/?wpdmc=boletim-municipal'
    ]
    start_date = date(2010, 12, 9)
    TERRITORY_ID = '3556701'

    # parse gazette pages dynamically
    def parse(self, response):
        pages = response.xpath('//*[@class="page-numbers"]//@href').getall()
        last_page = re.search(r'(paged=)(\d{,2})', pages[-1]).group(2)
        for i in range(1, int(last_page)+1):
             url = f'{self.start_urls[0]}&paged={i}'
             yield scrapy.Request(url, self.parse_page)

    # parse gazette links per gazette page
    def parse_page(self, response):
        dates = response.xpath('//td[@class="hidden-xs"]/text()').getall()
        dates = [parse(date, languages=['pt']).date() for date in dates]
        editions = response.xpath('//a[@class="package-title"]/text()')
        editionnum = [
            re.search(r'(ção|xtra|úmero)(\D*)(\d{1,4})', edition).group(3)
            for edition in editions.getall()
        ]
        extra = [
            True if re.search(r'[Ee]xtra', edition) else False
            for edition in editions.getall()
        ]
        links = response.xpath('//a[@rel="nofollow"]/@onclick').getall()
        links = [re.search(r'(htt(.)+)(\';)', link).group(1) for link in links]

        for date, edition, extra, link in zip(dates, editionnum, extra, links):
            if date >= self.start_date:
                yield Gazette(
                    date=date,
                    edition_number=edition,
                    file_urls=[link],
                    is_extra_edition=extra,
                    power='executive_legislative',
                    scraped_at=datetime.utcnow(),
                    territory_id=self.TERRITORY_ID,
                )
