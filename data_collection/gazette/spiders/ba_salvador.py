import datetime
import urllib.parse

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class BaSalvadorSpider(BaseGazetteSpider):
    TERRITORY_ID = "2927408"
    name = "ba_salvador"
    allowed_domains = ["salvador.ba.gov.br"]
    start_date = datetime.date(2001, 1, 1)

    def start_requests(self):
        initial_date = self.start_date.strftime("%Y-%m-%d")
        end_date = datetime.date.today().strftime("%Y-%m-%d")
        initial_search_parameters = {
            "filterTitle": "",
            "filterDateFrom": initial_date,
            "filterDateTo": end_date,
            "option": "com_dmarticlesfilter",
            "view": "articles",
            "Itemid": "3",
            "userSearch": "1",
            "limstart": "0",
        }
        encoded_params = urllib.parse.urlencode(initial_search_parameters)
        base_url = "http://www.dom.salvador.ba.gov.br/index.php"
        first_page_url = f"{base_url}?{encoded_params}"
        yield scrapy.Request(first_page_url)

    def parse(self, response):
        for gazette in response.css(".dmarticlesfilter_results_title"):
            gazette_date = gazette.css("#dmarticlesfilter_results_date::text").get()
            gazette_url = gazette.css("a::attr(href)").get()

            yield scrapy.Request(
                response.urljoin(gazette_url),
                cb_kwargs={"gazette_date": gazette_date},
                callback=self.parse_gazette,
            )

        for next_page_url in response.css(".paginacao a::attr(href)"):
            yield response.follow(next_page_url)

    def parse_gazette(self, response, gazette_date):
        gazette_date = datetime.datetime.strptime(gazette_date, "%Y-%m-%d").date()
        pdf_url = response.css("#PDFId embed::attr(src)").get()

        yield Gazette(
            date=gazette_date,
            file_urls=[pdf_url],
            power="executive",
            is_extra_edition=False,
        )
