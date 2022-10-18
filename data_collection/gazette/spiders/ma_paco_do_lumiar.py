import datetime as dt

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MaPacodoLumiarSpider(BaseGazetteSpider):

    # O Diário Oficial n° 117/2021 Legislativo não possui o PDF no link

    TERRITORY_ID = "2107506"
    name = "ma_paco_do_lumiar"
    start_date = dt.date(2017, 8, 3)
    end_date = dt.date.today()
    allowed_domains = ["pacodolumiar.ma.gov.br"]

    BASE_URL = "https://www.pacodolumiar.ma.gov.br/diariooficial.php"

    def start_requests(self):
        start_date = self.start_date.strftime("%d/%m/%Y")
        end_date = self.end_date.strftime("%d/%m/%Y")

        for i in range(1, 3):
            start_url = f"{self.BASE_URL}?descr=&esfera={i}&Num=&dtini={start_date}&dtfim={end_date}"
            yield Request(start_url)

    def parse(self, response):
        follow_next_page = True
        gazettes = response.css(".tab-pane.active .list-group-item")

        for gazette in gazettes:
            gazette_date = dt.datetime.strptime(
                gazette.css("span.calendarioIcon::text").get().replace(" ", ""),
                "%d/%m/%Y",
            ).date()

            if gazette_date < self.start_date:
                follow_next_page = False
                break

            url = gazette.css(".pull-right a::attr(href)").get()
            yield Request(response.urljoin(url), callback=self.extract_information)

        if (
            gazettes.xpath(
                "//div[@class='tab-pane active']//nav//ul//li/a[re:test(@aria-label, 'Next')]/span/i"
            ).get()
            is None
        ):
            follow_next_page = False

        if follow_next_page:
            next_page_url = gazettes.xpath(
                "//div[@class='tab-pane active']//nav//ul//li/a[re:test(@aria-label, 'Next')]/@href"
            ).getall()[-1]
            yield Request(f"{self.BASE_URL}{next_page_url}")

    def extract_information(self, response):
        is_extra_edition = False

        edition_number = (
            response.xpath("//div[@class='public_paginas']//h1/strong/text()")
            .get()
            .split(": ")[-1]
            .split("/")[0]
        )

        if edition_number.endswith("-A"):
            is_extra_edition = True

        power = (
            response.xpath(
                "//div[@class='public_paginas']//div[@class='row']//span/text()"
            )
            .get()
            .lower()
        )
        power = power.replace("o", "e")

        gazette_url = response.urljoin(
            response.xpath(
                "//div[@class='row']//div/a[re:test(@href, 'diario/')]/@href"
            ).get()
        )

        gazette_date = (
            response.xpath(
                "//div[@class='public_paginas']//div[@class='row']/div/text()"
            )
            .getall()[1]
            .replace(" ", "")
        )
        gazette_date = dt.datetime.strptime(gazette_date, "%d/%m/%Y").date()

        if gazette_url.endswith(".pdf"):
            yield Gazette(
                date=gazette_date,
                edition_number=edition_number,
                file_urls=[gazette_url],
                is_extra_edition=is_extra_edition,
                power=power,
            )
        else:
            pass
