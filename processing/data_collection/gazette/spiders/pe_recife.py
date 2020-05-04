"""Recife's gazettes spider

This spider is implemented to crawl Recife's `newest gazette system
<https://www.cepe.com.br/prefeituradiario/>`_. This system covers gazettes from 2017 to
current days. There is also a `deprecated system
<http://www.recife.pe.gov.br/diariooficial-acervo/>`_ which covers gazettes from 2001 to
2016 which is still not implemented.

Implementation details:
    The newest system presents gazettes in three ways:
        - Pagination:
            - Always available
            - Document is a gazette's page
            - Document is an image
        - Exporting:
            - Always available
            - Document can be a gazette's page or the entire gazette
            - Document is a PDF
            - Takes a long time to export and sometimes fails to do it on large gazettes
        - Attachment:
            - Sometimes available
            - When available, sometimes it's encrypted (so... not available)
            - Document is the entire gazette
            - Document is a PDF

    Because "Exporting" is unreliable, "Attachment" is chosen whenever possible and
    "Pagination" is the fallback.

    There weren't found any indications in the responses' content to differentiate extra
    from main editions and executive from legislative sections.

Gazettes examples:
    - `27/02/2018, main edition, 24 pages, with attachment, encrypted (.p7s)
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20180227&pasta=Fevereiro%5CDia%2027>`_
    - `27/07/2019, main edition, 32 pages, with attachment, not encrypted
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20190727&pasta=Julho\Dia%2027>_
    - `24/03/2020, extra edition, 16 pages, without attachment
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20200324&pasta=Marco%5CDia%2024>`_
    - `07/04/2020, main edition, 8 pages, without attachment
      <http://200.238.101.22/docreader/docreader.aspx?bib=R20200407&pasta=Abril\Dia%2007>`_
"""

import datetime as dt
import re

import dateparser
import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class PeRecifeSpider(BaseGazetteSpider):
    name = "pe_recife"
    TERRITORY_ID = "2611606"
    custom_settings = {"COOKIES_ENABLED": True, "AUTOTHROTTLE_ENABLED": True}

    AVAILABLE_DATES_URL = "https://www.cepe.com.br/prefeituradiario/diarios.txt"
    BASE_URL = (
        "http://200.238.101.22/docreader/docreader.aspx?"
        "bib=R{reversed_date}&pasta={month_full}%5CDia%20{day}"
    )
    PAGE_URL = (
        "http://200.238.101.22/docreader/cache/{session_id}/I{gazette_page_id}-2"
        "Alt={img_height}Lar={img_width}LargOri=003295AltOri=004299.JPG"
    )

    PAGE_PX_HEIGHT = 3295
    PAGE_PX_WIDTH = 4299

    months_full_names = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Marco",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }

    def start_requests(self):
        yield scrapy.Request(self.AVAILABLE_DATES_URL, self.fetch_gazette_initial_page)

    def fetch_gazette_initial_page(self, response):
        dates = self._parse_available_dates(raw_dates=response.text)

        for date in dates:
            url = self.BASE_URL.format(
                reversed_date=date.strftime("%Y%m%d"),
                month_full=self._month_full_name(date.month),
                day=date.strftime("%d"),
            )
            yield scrapy.Request(
                url,
                callback=self.request_main_page,
                meta={"date": date, "cookiejar": url},
            )

    def request_main_page(self, response):
        formdata = {
            "ScriptManager1": "DocumentoUpdatePanel|Timer1",
            "HiddenSize": f"{self.PAGE_PX_HEIGHT}x{self.PAGE_PX_WIDTH}",
            "__EVENTTARGET": "Timer1",
        }

        meta = response.meta.copy()
        meta.update(
            {
                "session_id": response.css("input[id=HiddenID]::attr(value)").get(),
                "gazette_id": response.css("input[id=hPagFis]::attr(value)").get(),
            }
        )

        yield scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            meta=meta,
            callback=self.choose_download_strategy,
            dont_filter=True,
        )

    def choose_download_strategy(self, response):
        if self._has_attachment(response) and not self._attachment_encrypted(response):
            yield from self.download_attachment(response)
        else:
            yield from self.request_pages(response)

    def download_attachment(self, response):
        href = response.css("a[href*=SendAttach]::attr(href)").get()
        req = scrapy.Request(response.urljoin(href), meta=response.meta)

        yield Gazette(
            date=response.meta["date"],
            file_urls=[req],
            territory_id=self.TERRITORY_ID,
            scraped_at=dt.datetime.utcnow(),
            power="executive_legislative",
        )

    def request_pages(self, response):
        total_pages = self._total_pages(
            response.css("span[id=PagTotalLbl]::text").get()
        )

        for i in range(total_pages):
            page = i + 1
            gazette_page_id = str(int(response.meta["gazette_id"]) + i)

            formdata = {
                "ScriptManager1": "PagUpdatePanel|PagAtualTxt",
                "HiddenSize": f"{self.PAGE_PX_HEIGHT}x{self.PAGE_PX_WIDTH}",
                "__EVENTTARGET": "PagAtualTxt",
                "PagAtualTxt": str(page),
                "hPagFis": gazette_page_id,
            }

            yield scrapy.FormRequest.from_response(
                response,
                formdata=formdata,
                meta=response.meta,
                callback=self.download_page,
                dont_filter=True,
            )

    def download_page(self, response):
        href = response.css("img[id=DocumentoImg]::attr(src)").get()
        req = scrapy.Request(response.urljoin(href), meta=response.meta)

        yield Gazette(
            date=response.meta["date"],
            file_urls=[req],
            territory_id=self.TERRITORY_ID,
            scraped_at=dt.datetime.utcnow(),
            power="executive_legislative",
        )

    def _parse_available_dates(self, raw_dates):
        available_dates = raw_dates.split("&")

        for date in filter(str.isdigit, available_dates):
            yield dateparser.parse(date, settings={"DATE_ORDER": "DMY"})

    def _month_full_name(self, month):
        month_str = str(month).zfill(2)
        return self.months_full_names[month_str]

    def _has_attachment(self, response):
        return True if response.css("input[id=AnexosBtn]") else False

    def _attachment_encrypted(self, response):
        attachment_url = response.xpath(
            "//span[@class='rmText'][contains(./text(), 'PrefeituradoRecife')]/text()"
        ).get()
        return ".p7s" in attachment_url

    def _total_pages(self, text):
        match = re.search("\d+", text)
        return int(match.group()) if match else None
