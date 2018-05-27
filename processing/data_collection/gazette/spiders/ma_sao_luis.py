# -*- coding: utf-8 -*-
# from dateparser import parse
import datetime as dt
import scrapy
from scrapy_splash import SplashRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaSaoLuisSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '2111300'
    name = 'ma_sao_luis'
    allowed_domains = ['www.semad.saoluis.ma.gov.br']
    start_urls = ['http://www.semad.saoluis.ma.gov.br:8090/easysearch/']

    def start_requests(self):
        lua_script = """
function main(splash, args)
    splash:go(args.url)
    getElementByXPath = splash:jsfunc([[
        function (path) {
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
    ]])
    splash:wait(4)
    tamanho_pagina = getElementByXPath("//tbody/tr/td/div[@class='GPFMNGWKN' and text()='20']")
    tamanho_pagina:mouse_click()
    tamanho_1 = getElementByXPath("//div[1]/div/span[@class='GPFMNGWKGC']")
    tamanho_1:mouse_click()
    splash:wait(2)
    return splash:html()
end
"""
        for url in self.start_urls:
            yield SplashRequest(
                url=url, callback=self.parse, endpoint='execute',
                args={'lua_source': lua_script})

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
