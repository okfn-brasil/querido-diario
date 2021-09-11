import datetime
import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjPetropolisSpider(BaseGazetteSpider):
    name = "rj_petropolis"
    TERRITORY_ID = "3303906"
    start_date = datetime.date(2001, 10, 2)
    allowed_domains = ["petropolis.rj.gov.br"]
    start_urls = [
        "https://www.petropolis.rj.gov.br/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/3.html"
    ]

    MESES_POR_EXTENSO = [
        "Dezembro",
        "Novembro",
        "Outubro",
        "Setembro",
        "Agosto",
        "Julho",
        "Junho",
        "Maio",
        "Abril",
        "Marco",
        "Março",
        "Fevereiro",
        "Janeiro",
    ]

    def parse(self, response):
        xpath_options = "//select[@name='cat_list']/option"
        options = response.xpath(xpath_options)
        for option in options:
            option_text = option.xpath("./text()").re_first(r"\w+")

            if option_text not in self.MESES_POR_EXTENSO:
                continue

            option_value = option.xpath("./@value").get()
            url = f"https://www.petropolis.rj.gov.br/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/{option_value}.html"
            yield scrapy.Request(url, callback=self.parse_editions)

    def parse_editions(self, response):
        xpath_links = "//a[@title='Download']"
        links = response.xpath(xpath_links)
        for link in links:
            url = response.urljoin(link.xpath("./@href").get())
            title = link.xpath("./text()")
            edition_number = title.re_first(r"\d+")
            date = re.search(r"-(\d+-de-[a-z]+-de-\d{4})", url).group(1)
            date = dateparser.parse(date, languages=["pt"]).date()
            is_extra_edition = "extra" in title.get().lower()
            yield Gazette(
                file_urls=[url],
                date=date,
                power="executive",
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
            )
