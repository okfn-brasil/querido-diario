from datetime import date

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    TERRITORY_ID = "3301702"
    name = "rj_duque_de_caxias"
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    start_urls = ["https://duquedecaxias.rj.gov.br"]
    base_url_before_2017 = "https://duquedecaxias.rj.gov.br/portal/boletim-oficial/{}/{}"
    base_url_after_2017 = "https://duquedecaxias.rj.gov.br/portal/{}.html"
    base_url_2021 = "https://duquedecaxias.rj.gov.br/portal/boletim-oficial.html"
    start_date = date(2013, 1, 1)

    month_names = [
        "Janeiro",
        "Fevereiro",
        "Marco",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    def start_requests(self):
        year = self.start_date.year
        if year > 2016:
            if year == 2021:
                url = self.base_url_2021
            else:
                url = self.base_url_after_2017.format(year)
            yield scrapy.Request(url)
        else:
            while year < 2017:
                month = self.start_date.month
                while month < len(self.month_names):
                    url = self.base_url_before_2017.format(
                        year, "{:02d}".format(month + 1) + "-" + self.month_names[month]
                    )
                    yield scrapy.Request(url)
                    month += 1
                year += 1


    def parse(self, response):
        if(response.status == 200):
            for element in response.xpath('//a[contains(@href,"pdf")]/@href'):
                if ".html" in response.url:
                    url = self.base_url + element.get()
                else:
                    url = response.url + element.get()
                extra_edition = False
                if element.get().lower() in "extraordionario":
                    extra_edition: True
                gazette_date = date.today()
                yield Gazette(
                    date=gazette_date,
                    file_urls=[url],
                    is_extra_edition=extra_edition,
                    power="executive_legislative",
                )
