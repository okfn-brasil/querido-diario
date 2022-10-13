import datetime as dt

import scrapy
from dateutil.rrule import DAILY, rrule
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaPacodoLumiarSpider(BaseGazetteSpider):
    TERRITORY_ID = "2107506"
    name = "ma_paco_do_lumiar"
    start_date = dt.date(2017, 8, 3)
    allowed_domains = ["pacodolumiar.ma.gov.br"]

    BASE_URL = "https://www.pacodolumiar.ma.gov.br/diariooficial.php"

    def start_requests(self):
        dates = rrule(freq=DAILY, dtstart=self.start_date, until=dt.date.today())
        for date in dates:
            yield Request(
                f"{self.BASE_URL}?descr=&esfera=0&Num=&dtini={date.day}%2F{date.month}%2F{date.year}&dtfim=&Exerc="
            )

    def parse(self, response):
        gazettes = response.css(".tab-pane.active").css(".list-group-item")
        root_url = "https://www.pacodolumiar.ma.gov.br/"
        for gazette in gazettes:
            gazette_date = dt.datetime.strptime(
                gazettes.css("span.calendarioIcon::text").get().replace(" ", ""),
                "%d/%m/%Y",
            ).date()
            edition_number = (
                gazettes.xpath("//span/strong/text()")
                .get()
                .split(": ")[1]
                .split("/")[0]
            )
            gazette_next_url = gazettes.css(".pull-right a::attr(href)").get()

            yield scrapy.Request(f"{root_url}{gazette_next_url}")

            pdf_url = (
                response.css(".public_paginas .row .btn.btn-primary")
                .css("a::attr(href)")
                .get()
            )
            gazette_url = f"{root_url}{pdf_url}"

            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=gazette_url,
                is_extra_edition=False,
                power="executive",
            )
