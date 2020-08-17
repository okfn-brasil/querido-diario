# -*- coding: utf-8 -*-
from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette


class MsCampoGrandeSpider(scrapy.Spider):
    MUNICIPALITY_ID = "5002704"
    name = "ms_campo_grande"
    allowed_domains = ["portal.capital.ms.gov.br"]

    def start_requests(self):
        today = dt.date.today()
        next_year = today.year + 1
        for year in range(2015, next_year):
            for month in range(1, 13):
                if year == today.year and month > today.month:
                    return

                yield scrapy.FormRequest(
                    url="http://portal.capital.ms.gov.br/diogrande/diarioOficial",
                    method="POST",
                    formdata={"mes": str(month), "ano": str(year)},
                )

    def parse(self, response):
        year = response.css("#leftToRight > h3").extract_first().split("/")[1]
        docs = response.css(".arquivos li")
        for doc in docs:
            url = doc.css(".inner-detail a::attr(href)").extract_first()
            day = doc.css(".day strong::text").extract_first()
            month = doc.css(".month::text").extract_first()
            date = parse(f"{day}/{month}/{year}", languages=["pt"]).date()
            doc_title = doc.css(".inner-detail::text").extract_first().lower()
            is_extra_edition = "extra" in doc_title or "suplemento" in doc_title
            power = "executive_legislature"
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                municipality_id=self.MUNICIPALITY_ID,
                power=power,
                scraped_at=dt.datetime.utcnow(),
            )
