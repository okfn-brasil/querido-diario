# -*- coding: utf-8 -*-
import datetime as dt

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class SpSantosSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3548500'
    name = 'sp_santos'
    allowed_domains = ['santos.sp.gov.br']
    start_urls = ['https://diariooficial.santos.sp.gov.br/']
    download_url = 'https://diariooficial.santos.sp.gov.br/edicoes/inicio/download/{}'

    def parse(self, response):
        """
        @url https://diariooficial.santos.sp.gov.br/
        @returns items 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        # all of the dates with gazettes are available inside the following hidden textarea:
        dates = response.css('#datas.hidden::text').extract_first()

        start_date = dt.date(2015, 1, 1)
        parsing_date = dt.date.today()
        while parsing_date >= start_date:
            if str(parsing_date) in dates:
                url = self.download_url.format(parsing_date)
                yield Gazette(
                    date=parsing_date,
                    file_urls=[url],
                    is_extra_edition=False,
                    municipality_id=self.MUNICIPALITY_ID,
                    power='executive_legislature',
                    scraped_at=dt.datetime.utcnow()
                )

            parsing_date = parsing_date - dt.timedelta(days=1)
