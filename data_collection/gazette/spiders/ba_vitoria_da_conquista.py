from datetime import date

import scrapy
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaVitoriaDaConquistaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2933307"
    name = "ba_vitoria_da_conquista"
    allowed_domains = ["pmvc.ba.gov.br"]
    start_urls = ["https://dom.pmvc.ba.gov.br/"]
    start_date = date(2013, 1, 1)

    def start_requests(self):
        url = "https://dom.pmvc.ba.gov.br/diarios/{year}/{month}"
        for year in range(self.start_date.year, self.end_date.year + 1):
            for month in range(1, 13):
                yield scrapy.Request(url.format(year=year, month=month))

    def parse(self, response):
        """
        Extracts the gazette items from the web page.
        """
        boxes = response.css(".box-diario")
        links_xpath = './/a[text()[normalize-space(.) = "Visualizar Diário"]]/@href'
        for box in boxes:
            parsing_date = box.re(r"diario-(\d{8})")[0]
            parsing_date = parse(parsing_date, date_formats=["%Y%m%d"]).date()
            url = box.xpath(links_xpath).extract_first()
            url = url.replace("previsualizar", "baixar")
            if self.start_date <= parsing_date <= self.end_date:
                yield Gazette(
                    date=parsing_date,
                    edition_number=(box.css("h1::text").re_first(r"Edição (\S*)")).replace(".", ""),
                    file_urls=[url],
                    is_extra_edition=False,
                    power="executive_legislative",
                )
