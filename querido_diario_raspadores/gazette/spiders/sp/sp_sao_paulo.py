from datetime import date
from urllib.parse import urlparse

import filetype
import scrapy
from dateparser import parse
from scrapy import signals
from scrapy.exceptions import StopDownload

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.blocking import is_cloudflare_challenge


class SpSaoPauloSpider(BaseGazetteSpider):
    TERRITORY_ID = "3550308"
    name = "sp_sao_paulo"
    start_date = date(2017, 6, 1)
    allowed_domains = ["diariooficial.prefeitura.sp.gov.br"]
    start_urls = [
        "https://diariooficial.prefeitura.sp.gov.br/"
        "md_epubli_controlador.php?acao=memoria_listar"
    ]

    # The site uses F5 protection and may require the proxy in production.
    zyte_smartproxy_enabled = False

    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 5,
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.pdf_headers_received, signal=signals.headers_received
        )
        crawler.signals.connect(
            spider.pdf_bytes_received, signal=signals.bytes_received
        )
        return spider

    def pdf_headers_received(self, headers, body_length, request, spider):
        if request.meta.get("check_pdf"):
            # Reset for every response, including retries and redirects.
            request.meta["pdf_bytes_received"] = 0

    def pdf_bytes_received(self, data, request, spider):
        if not request.meta.get("check_pdf"):
            return
        received = request.meta.get("pdf_bytes_received", 0) + len(data)
        request.meta["pdf_bytes_received"] = received
        if received >= 8192:
            # Keep the partial response for parse_pdf; files download fully.
            raise StopDownload(fail=False)

    def parse(self, response):
        if self.start_date > self.end_date:
            return

        for year_option in response.css(".mandato-ano"):
            year = int(year_option.css("::text").get())
            year_formkey = year_option.attrib["data-value"]

            if self.start_date.year <= year <= self.end_date.year:
                for month in range(1, 13):
                    if (
                        (self.start_date.year, self.start_date.month)
                        <= (year, month)
                        <= (self.end_date.year, self.end_date.month)
                    ):
                        yield scrapy.FormRequest.from_response(
                            response,
                            formid="frmEpubliMemoria",
                            formdata={
                                "hdnFiltroMandato": year_formkey,
                                "hdnFiltroAno": str(year),
                                "hdnFiltroMes": str(month),
                                "hdnInicio": "0",
                            },
                            callback=self.parse_editions,
                        )

    def parse_editions(self, response):
        for item in response.css(".painelEdições.clearfix a"):
            gazette_url = item.attrib["href"]
            gazette_url = (
                urlparse(response.urljoin(gazette_url))
                ._replace(scheme="https")
                .geturl()
            )
            raw_date = "/".join(item.css(".legenda h3::text").getall())
            edition_date = parse(raw_date, languages=["pt"]).date()

            if self.start_date <= edition_date <= self.end_date:
                yield scrapy.Request(
                    gazette_url,
                    callback=self.parse_pdf,
                    meta={"check_pdf": True},
                    cb_kwargs={"edition_date": edition_date},
                )

    def parse_pdf(self, response, edition_date):
        # Reuse the pipeline's file-header detection, not the server MIME type.
        body = response.body[:8192]
        if is_cloudflare_challenge(response) or b"TSPD" in body or b"bobcmn" in body:
            self.logger.error("Anti-bot challenge (F5/Cloudflare): %s", response.url)
            return

        kind = filetype.guess(response.body[:261])
        if response.status != 200 or kind is None or kind.extension != "pdf":
            self.logger.error("Invalid gazette: expected PDF at %s", response.url)
            return

        yield Gazette(
            date=edition_date,
            file_urls=[response.url],
            edition_number="",
            is_extra_edition=False,
            power="executive",
        )
