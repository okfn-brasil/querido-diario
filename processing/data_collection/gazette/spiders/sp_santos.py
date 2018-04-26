# -*- coding: utf-8 -*-
from dateparser import parse
import datetime as dt
import json
import scrapy

from gazette.items import Gazette

class SpSantosSpider(scrapy.Spider):
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
        delta = dt.timedelta(days=1)
        while start_date <= dt.date.today():
            if str(start_date) in dates:
                url = self.download_url.format(start_date)
                yield Gazette(
                    date=start_date,
                    file_urls=[url],
                    is_extra_edition=False,
                    municipality_id=self.MUNICIPALITY_ID,
                    scraped_at=dt.datetime.utcnow(),
                    power='executive_legislature'
                )

            start_date += delta
