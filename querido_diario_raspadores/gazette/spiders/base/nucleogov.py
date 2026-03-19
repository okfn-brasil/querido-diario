from urllib.parse import urlparse

import scrapy
from scrapy.exceptions import NotConfigured

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.nucleogov import DiarioPage


class BaseNucleoGovSpider(BaseGazetteSpider):
    url_api_path = "/api/diarios"
    per_page = 100

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "base_url"):
            raise NotConfigured("Please set a value for `base_url`")

        self.allowed_domains = [urlparse(self.base_url).netloc]

        super().__init__(*args, **kwargs)

    def start_requests(self):
        s3_domain = self.crawler.settings.get(
            "NUCLEOGOV_S3_DOMAIN",
            "diariooficial.s3.us-east-2.amazonaws.com",
        )
        self.allowed_domains.append(s3_domain)

        yield scrapy.Request(
            url=self._build_url(page=1),
            callback=self.parse,
        )

    def _build_url(self, page):
        return (
            f"{self.base_url}{self.url_api_path}"
            f"?situacao=2&per_page={self.per_page}&page={page}"
        )

    def parse(self, response):
        page = DiarioPage.from_response(response)

        for diario in page.diarios:
            if diario.data < self.start_date or diario.data > self.end_date:
                continue

            if not diario.file_urls:
                continue

            yield Gazette(
                date=diario.data,
                edition_number=diario.numero,
                file_urls=diario.file_urls,
                is_extra_edition=diario.is_extra_edition,
                power="executive",
            )

        if page.has_next_page:
            yield scrapy.Request(
                url=self._build_url(page=page.next_page),
                callback=self.parse,
            )
