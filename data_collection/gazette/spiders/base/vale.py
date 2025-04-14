from re import findall

import scrapy
import scrapy.resolver
from dateparser import parse

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class ValeGazetteSpider(BaseGazetteSpider):
    """
    Base spider for cities using the Framework Vale as design system.
    """

    def start_requests(self):
        yield scrapy.Request(url=self._get_url(page=1), callback=self._parse_pagination)

    def _parse_pagination(self, response):
        last_page = response.css('[title="Última página"] ::attr(href)').get()
        if last_page:
            number_last_page = int(last_page.split("/")[-1])
        else:
            number_last_page = 0
        for i in range(number_last_page + 1):
            yield scrapy.Request(self._get_url(page=i))

    def _get_url(self, page):
        start_date = self.start_date.strftime("%Y-%m-%d")
        end_date = self.end_date.strftime("%Y-%m-%d")
        url = (
            f"https://{self.allowed_domains[0]}/diariooficial/"
            f"pesquisa/all/all/{start_date}/{end_date}/{page}"
        )
        return url

    def _get_gazette_date(self, gazette):
        publish_date = gazette.xpath('.//*[contains(text(), "Publicado")]/text()').get()
        website_date = publish_date.split(",")[1]
        datetime_date = parse(website_date, languages=["pt"]).date()
        return datetime_date

    def parse(self, response):
        gazettes = response.css(".ant-list-item")

        for gazette in gazettes:
            gazette_date = self._get_gazette_date(gazette)
            file_url = gazette.css("a ::attr(href)").get()
            edition_text = "".join(gazette.css(".edition-number ::text").getall())
            edition_number = findall(r"(\d+)", edition_text)[0]
            is_extra_edition = "Extra" in edition_text
            yield Gazette(
                date=gazette_date,
                file_urls=[file_url],
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive",
            )
