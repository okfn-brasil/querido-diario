# -*- coding: utf-8 -*-
import datetime as dt
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PiParnaibaSpider(BaseGazetteSpider):
    TERRITORY_ID = "2207702"
    name = "pi_parnaiba"
    start_urls = ["http://dom.parnaiba.pi.gov.br/"]
    DATE_FORMAT = "%d/%m/%Y"
    
    def convert_str_to_date(self,data):
        date = dt.datetime.strptime(data, self.DATE_FORMAT).date()
        return date
    
    def change_date_order(self,date):
        date_format = "/".join(date.split('/')[::-1])
        return date_format

    def parse(self, response):
        urls = response.xpath('//ul[@class="pagination"]//a/@href').extract()
        gazette_info = response.xpath('//div[@class="table-responsive"]//tbody/tr')

        for info in gazette_info:
            edition_number, data, filename = info.xpath("td/text()").extract()
            date = dt.datetime.strptime(data, "%d-%m-%Y").date()
            if date < self.start_date:
                return
            is_extra_edition = "extra" in filename.lower()
            link = info.xpath("td/a/@href").extract_first()
            url = response.urljoin(link)
            yield Gazette(
                file_urls=[url],
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

        for next_page in urls:
            yield Request(next_page, callback=self.parse)
