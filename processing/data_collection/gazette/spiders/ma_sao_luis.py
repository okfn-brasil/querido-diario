# -*- coding: utf-8 -*-
import dateparser
import datetime as dt
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
    splash:wait(6)
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
        date = response.xpath(("//body/div/div/div/div/div/div/div/div/div"
                               "/div/div/div/div/div/"
                               "table/tbody/tr[1]/td[2]/div/text()"))
        date = date.extract_first()
        date = dateparser.parse(date)
        if date.year < 2015:
            raise StopIteration

        url = response.xpath(("//tbody/tr[4]/td[1]/a"
                              "[@class='campoResultadoDownload']"
                              "/@href")).extract_first()
        url = response.url[:39] + url
        yield Gazette(
            date=date,
            file_urls=[url],
            is_extra_edition=False,
            municipality_id=self.MUNICIPALITY_ID,
            scraped_at=dt.datetime.utcnow(),
            power='executive'
        )
        lua_script = """
function main(splash, args)
    getElementByXPath = splash:jsfunc([[
        function (path) {
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
    ]])
    link_next = getElementByXPath("//img[@style='width:16px;height:16px;background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAhElEQVR42uWRMQpDIRAFva1X8AYWgoLYWFopdhYiHkGsrD3MCyukzzdNIANbzvBExn6S1hq+CtRakVK6j5RSsPe+j+ScT2DOCa3180iMEWst9N7PPY6EEDDGOLK1FlJKCCE+j3jvQT/xljnnzxY450ArrmTCGHPefSUTSql7maDp7H94AVSkZqN2tVRLAAAAAElFTkSuQmCC) no-repeat 0px 0px;']")
    link_next:mouse_click()
    splash:wait(3)
    return splash.html()
end
"""
        print('===================== clicked next')
        yield SplashRequest(
            url=response.url, callback=self.parse, endpoint='execute',
            args={'lua_source': lua_script})
