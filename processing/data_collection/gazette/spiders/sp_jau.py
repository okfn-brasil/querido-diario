# -*- coding: utf-8 -*-
from scrapy import Spider
from gazette.items import Gazette
from datetime import datetime
import dateparser


class SpJauSpider(Spider):
    TERRITORY_ID = "3525300"
    name = "sp_jau"
    allowed_domains = ["jau.sp.gov.br"]
    start_urls = ["http://www.jau.sp.gov.br/jornal-oficial"]

    def parse(self, response):
        gazettes_selector = response.xpath("//div[@id='concursos']")

        for gazette_selector in gazettes_selector:
            date = dateparser.parse(
                gazette_selector.xpath(".//p/text()")
                .get()
                .strip()
                .split(" ")[0]
                .strip(),
                date_formats=["%d/%m/%Y"],
            ).date()
            url = response.urljoin(gazette_selector.xpath(".//a/@href").get())
            gazette_title = gazette_selector.xpath(".//h2/text()").get().lower()

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition="extra" in gazette_title,
                territory_id=self.TERRITORY_ID,
                scraped_at=datetime.utcnow(),
                power="executive",
            )
