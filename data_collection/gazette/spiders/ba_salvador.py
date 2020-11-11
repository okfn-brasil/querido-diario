import datetime
import re
import urllib.parse

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.settings import ITEM_PIPELINES
from gazette.spiders.base import BaseGazetteSpider


class BaSalvadorSpider(BaseGazetteSpider):
    TERRITORY_ID = "2927408"
    name = "ba_salvador"
    allowed_domains = ["salvador.ba.gov.br"]
    power = "executive"
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
            gazette_date = gazette.css(
                "#dmarticlesfilter_results_date::text"
            ).extract_first("")
            gazette_url = gazette.css("a::attr(href)").extract_first()

            yield scrapy.Request(
                response.urljoin(gazette_url),
                meta={"gazette_date": gazette_date},
                callback=self.parse_gazette,
            )

        for next_page_url in response.css(".paginacao a::attr(href)"):
            yield response.follow(next_page_url)

    def parse_gazette(self, response):
        parsed_date = dateparser.parse(
            response.meta.get("gazette_date"), settings={"DATE_ORDER": "YMD"}
        )
        pdf_url = response.css("#PDFId embed::attr(src)").extract_first()

        yield Gazette(
            date=parsed_date.date(),
            file_urls=[pdf_url],
            power=self.power,
            is_extra_edition=False,
        )
