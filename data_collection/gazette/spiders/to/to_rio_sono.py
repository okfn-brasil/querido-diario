import json
import re
from datetime import datetime

import scrapy
from scrapy.http import HtmlResponse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ToRioSonoSpider(BaseGazetteSpider):
    TERRITORY_ID = "1718758"
    name = "to_rio_sono"
    allowed_domains = ["riosono.to.gov.br"]

    custom_settings = {
        "MEDIA_ALLOW_REDIRECTS": True,
    }
    BASE_URL = "https://riosono.to.gov.br/wp-admin/admin-ajax.php?"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://riosono.to.gov.br",
        "Alt-Used": "riosono.to.gov.br",
        "Connection": "keep-alive",
        "Referer": "https://riosono.to.gov.br/diario-oficial/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    current_page = 0
    pages_num = None
    ITEMS_PER_PAGE = 100

    def start_requests(self):
        url = "https://riosono.to.gov.br/diario-oficial/"
        yield scrapy.Request(url)

    def _translate_month(self, month):
        return {
            "janeiro": "01",
            "fevereiro": "02",
            "março": "03",
            "abril": "04",
            "maio": "05",
            "junho": "06",
            "julho": "07",
            "agosto": "08",
            "setembro": "09",
            "outubro": "10",
            "novembro": "11",
            "dezembro": "12",
        }[month]

    def _get_date_from_parent_edition(self, gazette_text):
        gazette_text = json.loads(f'"{gazette_text}"').lower().replace("1º", "01")
        pattern = r"(0[1-9]|[12][0-9]|3[01]) de (janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) de ([0-9]{4})"

        match = re.search(pattern, gazette_text)

        if match:
            raw_date = f"{str(match.group(1))}-{self._translate_month(str(match.group(2)))}-{str(match.group(3))}"
            return datetime.strptime(str(raw_date), "%d-%m-%Y").date()

    def _get_edition_from_name(self, gazette_name):
        decoded_str = json.loads(f'"{gazette_name}"')
        pattern = r"nº\s+(\d+)"

        match = re.search(pattern, decoded_str)

        if match:
            return match.group(1)

    def parse(self, response):
        if not self.pages_num:
            self.pages_num = response.xpath("//div[@data-pages]/@data-pages").get()
            self.ITEMS_PER_PAGE = int(self.pages_num) * 10
        else:
            normalized_text_response = re.sub(r'\\(["\'\\/])', r"\1", response.text)
            response = HtmlResponse(
                url=self.BASE_URL, body=normalized_text_response, encoding="utf-8"
            )
            if self.is_body_empty(response):
                return
            urls = response.css(".elementor-icon-list-item a")
            gazettes = response.css(".elementor-size-default::text")
            for gazette, url in zip(gazettes, urls):
                url = url.css("a::attr(href)").get()
                gazette_edition = self._get_edition_from_name(gazette.get())
                gazette_date = self._get_date_from_parent_edition(gazette.get())
                item = Gazette(
                    power="executive_legislative",
                    date=gazette_date,
                    edition_number=gazette_edition,
                    file_urls=[url],
                )
                yield item
        self.current_page += 1
        yield self.make_request(self.current_page)

    def make_request(self, page_num):
        return scrapy.Request(
            self.BASE_URL,
            method="POST",
            headers=self.headers,
            dont_filter=True,
            body=self.make_body(page_num),
            callback=self.parse,
        )

    def make_body(self, page):
        body_message = (
            f"""action=jet_smart_filters&provider=jet-engine/pesquisadiariooficial\
        &settings[lisitng_id]=288&settings[_element_id]=pesquisadiariooficial&props[page]={page}\
        &paged={page}&settings[posts_num]={self.ITEMS_PER_PAGE}""".replace(
                "/", "%2F"
            )
            .replace("[", "%5B")
            .replace("]", "%5D")
            .replace(" ", "")
        )
        return f"{body_message}"

    def is_body_empty(self, response):
        no_data_element = response.css(".jet-listing-not-found::text").get()

        if no_data_element and "No data was found" in no_data_element:
            return True

        return False
