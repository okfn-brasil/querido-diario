# -*- coding: utf-8 -*-
# from dateparser import parse
import datetime as dt
# import json
import scrapy

from gazette.items import Gazette


class MaSaoLuisSpider(scrapy.Spider):
    MUNICIPALITY_ID = '2111300'
    name = 'ma_sao_luis'
    allowed_domains = ['www.semad.saoluis.ma.gov.br']
    start_urls = ['http://www.semad.saoluis.ma.gov.br:8090/easysearch/']
    download_url = 'https://gov.br/'

    def parse(self, response):
        """
        @url
        @returns items 1
        @scrapes date file_urls is_extra_edition
                 municipality_id power scraped_at
        """
        # dates with gazettes available inside the following hidden textarea:
        dates = response.css('#datas.hidden::text').extract_first()

        start_date = dt.date()
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
                    power='executive'
                )

            start_date += delta
