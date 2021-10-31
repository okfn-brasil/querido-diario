import re
import urllib
from datetime import date, timedelta

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class MgMontesClarosSpider(BaseGazetteSpider):
    TERRITORY_ID = "3143302"
    name = "mg_montes_claros"
    allowed_domains = ["diariooficial.montesclaros.mg.gov.br"]
    start_url = "https://diariooficial.montesclaros.mg.gov.br"
    start_date = date(2013, 7, 2)

    EXTRA_EDITION_MARK = "EDIÇÃO EXTRA"
    AFTER_2015_URL_FORMAT = "https://diariooficial.montesclaros.mg.gov.br/exercicio-%d"
    YEAR_MONTH_URL_FORMAT = "https://diariooficial.montesclaros.mg.gov.br/%d/%s"
    BEFORE_2016_URL_FORMAT = (
        "https://diariooficial.montesclaros.mg.gov.br/%d/edicoes-de-%d"
    )

    PDFLINK_REGEX = re.compile("^.*(https://[^']+\\.pdf).*$", re.IGNORECASE)
    MONTHS = [
        "janeiro",
        "fevereiro",
        "marco",
        "abril",
        "maio",
        "junho",
        "julho",
        "agosto",
        "setembro",
        "outubro",
        "novembro",
        "dezembro",
    ]

    def start_requests(self):
        begin = self.start_date.year
        end = self.end_date.year

        for year in range(begin, end + 1):
            if year > 2017:
                requests = self.search_by_year(year)
            elif year == 2017 or year == 2016:
                requests = self.search_by_month(year)
            else:
                requests = self.get_by_year(year)

            for request in requests:
                yield request

    def search_by_year(self, year):
        url = self.AFTER_2015_URL_FORMAT % (year)
        yield Request(url, callback=self.parse_by_year)

    def get_by_year(self, year):
        url = self.BEFORE_2016_URL_FORMAT % (year, year)
        yield Request(url, callback=self.parse_html_with_links)

    def search_by_month(self, year):
        for month in range(12):
            month_begin = date(year, month + 1, 1)
            if month_begin < self.start_date:
                continue

            end_month = (month_begin + timedelta(days=32)).replace(day=1)
            if end_month > self.end_date:
                continue

            url = self.YEAR_MONTH_URL_FORMAT % (year, self.MONTHS[month])
            yield Request(url, callback=self.parse_html_with_links)

    def parse_link(self, link):
        title = link.css("*::text").extract_first()
        url = link.xpath("@href").extract_first()

        link_date = link.re_first("([0-9]{2}/[0-9]{2}/[0-9]{4})")
        gazette_date = dateparser.parse(link_date, settings={"DATE_ORDER": "DMY"})
        gazette_date = gazette_date.date()

        if gazette_date < self.start_date:
            return None
        if gazette_date > self.end_date:
            return None

        is_extra = self.EXTRA_EDITION_MARK in title.upper()

        return Request(
            url,
            meta={"date": gazette_date, "is_extra_edition": is_extra},
            callback=self.get_link_javascript,
        )

    def parse_by_year(self, response):
        links = response.xpath('//a[contains(@href, "/diario-oficial-eletronico")]')

        for link in links:
            request = self.parse_link(link)
            if request is not None:
                yield request

    def get_link_javascript(self, response):
        js = response.xpath("//script").extract_first()

        match = self.PDFLINK_REGEX.match(js)
        if not match:
            return

        link = match.group(1)
        return Gazette(
            date=response.meta["date"],
            file_urls=[link],
            is_extra_edition=response.meta["is_extra_edition"],
            power="executive_legislative",
        )

    def parse_html_with_links(self, response):
        links = response.xpath(
            '//a[contains(@href, "%s")]'
            % (urllib.parse.quote("Diário Oficial Eletrônico"))
        )

        for link in links:
            title = link.css("*::text").extract_first()
            url = link.xpath("@href").extract_first()
            url = url.replace("http://", "https://")

            link_date = link.re_first("([0-9]{2}-[0-9]{2}-[0-9]{2})")
            gazette_date = dateparser.parse(link_date, settings={"DATE_ORDER": "DMY"})
            gazette_date = gazette_date.date()

            is_extra_edition = self.EXTRA_EDITION_MARK in title.upper()

            yield Gazette(
                date=gazette_date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )
