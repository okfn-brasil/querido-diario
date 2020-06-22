"""Recife's gazettes spider

This spider is implemented to crawl Recife's `newest gazette system
<https://www.cepe.com.br/>`_. This system covers gazettes from 2017 to
current days. There is also a `deprecated system
<http://www.recife.pe.gov.br/diariooficial-acervo/>`_ which covers gazettes from 2001 to
2016 which is still not implemented.

Implementation details:
    The spider get all dates with gazettes published fetching the diarios.txt
    file. Using this data, it generates the url for the files hosted in the
    CEPE website.


Gazettes examples:
    - http://200.238.105.211/cadernos/2020/20200613/8-PrefeituradoRecife/PrefeituradoRecife(20200613).pdf
    - http://200.238.105.211/cadernos/2020/20200616/8-PrefeituradoRecife/PrefeituradoRecife(20200616).pdf
    - http://200.238.105.211/cadernos/2020/20200618/8-PrefeituradoRecife/PrefeituradoRecife(20200618).pdf

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

    AVAILABLE_DATES_URL = "https://www.cepe.com.br/prefeituradiario/diarios.txt"
    BASE_URL = "http://200.238.105.211/cadernos/{full_year}/{full_date}/8-PrefeituradoRecife/PrefeituradoRecife({full_date}).pdf"

    def start_requests(self):
        # first request just get the txt file with all available dates
        yield scrapy.Request(self.AVAILABLE_DATES_URL, self.parse_diarios_file)

    def parse_diarios_file(self, response):
        """
        Callback function called to parse the diarios.txt file
        """
        # Parse the dates available and return a request for get the page for
        # each one
        dates = self._parse_available_dates(raw_dates=response.text)

        # generate the gazette item for each date found
        for date in dates:
            url = self.BASE_URL.format(
                full_date=date.strftime("%Y%m%d"), full_year=date.strftime("%Y"),
            )
            self.log(url)
            yield Gazette(
                date=date,
                file_urls=[url],
                territory_id=self.TERRITORY_ID,
                scraped_at=dt.datetime.utcnow(),
                power="executive_legislative",
            )

    def _parse_available_dates(self, raw_dates):
        """
        Parses the diarios.txt file.

        This generator method gets the string of the diarios.txt file get
        from the gazette site and parses it into date objects.

        Returns dates found in the diarios.txt file
        """
        available_dates = raw_dates.split("&")
        for date in filter(str.isdigit, available_dates):
            yield dateparser.parse(date, settings={"DATE_ORDER": "DMY"})
