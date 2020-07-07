from dateparser import parse
from datetime import datetime

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class AlMaceioSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = "2704302"
    name = "al_maceio"
    allowed_domains = ["maceio.al.gov.br"]
    start_urls = ["http://www.maceio.al.gov.br/noticias/diario-oficial/"]
    page_number = 1

    def parse(self, response):
        gazettes = list(response.xpath("//article"))
        for gazette in gazettes:
            url = gazette.xpath("a/@href").extract_first()

            if not url:  # In some cases the href attr is empty, e.g. 24-11-2015
                continue

            date_str = gazette.xpath("time/text()").extract_first()
            date = parse(date_str, languages=["pt"])
            title = gazette.xpath("a/@title").extract_first()
            is_extra_edition = "suplemento" in (title.lower())

            if "wp-content/uploads" in url:
                gazette = self.create_gazette(date, url, is_extra_edition)
                yield gazette
            else:
                request = scrapy.Request(url, self.parse_additional_page)
                request.meta["date"] = date
                request.meta["is_extra_edition"] = is_extra_edition
                yield request

        """
        This condition is necessary to stop crawling when there are no more gazettes
        """
        if gazettes:
            self.page_number += 1
            yield scrapy.Request(
                "{0}/page/{1}".format(self.start_urls[0], str(self.page_number))
            )

    def parse_additional_page(self, response):
        url = response.xpath('//p[@class="attachment"]/a/@href').extract_first()
        gazette = self.create_gazette(
            response.meta["date"], url, response.meta["is_extra_edition"]
        )
        yield gazette

    def create_gazette(self, date, url, is_extra_edition):
        return Gazette(
            date=date,
            file_urls=[url],
            is_extra_edition=is_extra_edition,
            municipality_id=self.MUNICIPALITY_ID,
            power="executive_legislature",
            scraped_at=datetime.utcnow(),
        )
