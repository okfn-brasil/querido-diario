# -*- coding: utf-8 -*-
from dateparser import parse
import datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PrCascavelSpider(BaseGazetteSpider):
    TERRITORY_ID = '4104808'
    name = 'pr_cascavel'
    allowed_domains = ['cascavel.pr.gov.br']
    start_urls = ['http://www.cascavel.pr.gov.br/servicos/orgao_oficial.php']
    download_url = 'http://www.cascavel.pr.gov.br/anexos/{}'

    def parse(self, response):
        """
        @url http://www.cascavel.pr.gov.br/servicos/orgao_oficial.php
        @returns items 1
        @scrapes date file_urls is_extra_edition territory_id power scraped_at
        """
        for row in response.css('table tr')[1:]:
            cols = row.css('td')
            edition = cols[0].css('font::text').extract()
            date = cols[1].css('font::text').extract_first()
            date = parse(date, languages=['pt']).date()
            for link in cols[2].css('a'):
                link_text = link.css('::text').extract_first()
                power = 'executive' if 'Executivo' in link_text else 'legislature'
                url = link.css('::attr(href)').extract_first()[10:]
                url = self.download_url.format(url)
                yield Gazette(
                    date=date,
                    file_urls=[url],
                    is_extra_edition=False,
                    territory_id=self.TERRITORY_ID,
                    power=power,
                    scraped_at=dt.datetime.utcnow()
                )
        xpath = '//a[@title="Próxima página"]/@href'
        next_page_url = response.xpath(xpath).extract_first()
        if next_page_url:
            yield response.follow(next_page_url)
