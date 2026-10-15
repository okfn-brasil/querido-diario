import re
from datetime import date, datetime
from urllib.parse import unquote

from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence, yearly_sequence


class MgMontesClarosSpider(BaseGazetteSpider):
    TERRITORY_ID = "3143302"
    name = "mg_montes_claros"
    allowed_domains = ["montesclaros.mg.gov.br"]
    start_date = date(2013, 7, 2)

    BASE_URL = "https://diariooficial.montesclaros.mg.gov.br"
    MONTHS = (
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
    )
    # Digit lookarounds keep four-digit years out of the two-digit-year match
    DATE_PATTERNS = (
        (re.compile(r"diario-oficial-eletronico-(\d{8})"), "%d%m%Y"),
        (re.compile(r"(?<!\d)(\d{2}/\d{2}/\d{4})"), "%d/%m/%Y"),
        (re.compile(r"(?<!\d)(\d{2}-\d{2}-\d{2})(?!\d)"), "%d-%m-%y"),
        # Some slugs lost the year's last digit; the URL path still has the year
        (re.compile(r"(\d{4})/[a-z]+/diario-oficial-eletronico-(\d{4})"), "%Y%d%m"),
    )
    # Old listings still link to a retired host that now times out
    RETIRED_HOST = re.compile(
        r"^https?://(www\.)?montesclaros\.mg\.gov\.br/diariooficial/"
    )
    UPLOAD_URL = f"{BASE_URL}/upload/diario-oficial/files/edicoes/"
    EXTRA_EDITION = re.compile(r"EDI[CÇ][AÃ]O\W*EXTRA")

    async def start(self):
        for year in yearly_sequence(self.start_date, self.end_date):
            # The site keeps each period in the layout it was published with
            if year <= 2015:
                yield Request(
                    f"{self.BASE_URL}/{year}/edicoes-de-{year}",
                    callback=self.parse_pdf_listing,
                )
            elif year <= 2017:
                first_day = max(self.start_date, date(year, 1, 1))
                last_day = min(self.end_date, date(year, 12, 31))
                for month in monthly_sequence(first_day, last_day):
                    yield Request(
                        f"{self.BASE_URL}/{year}/{self.MONTHS[month.month - 1]}",
                        callback=self.parse_pdf_listing,
                    )
            else:
                yield Request(
                    f"{self.BASE_URL}/exercicio-{year}", callback=self.parse_editions
                )

    def parse_pdf_listing(self, response):
        # Budget-law annexes share the folder; only gazette filenames carry this
        links = response.css('a[href*="Oficial%20Eletr"]')
        for link, gazette_date, is_extra_edition in self._dated_links(links):
            yield Gazette(
                date=gazette_date,
                file_urls=[
                    self.RETIRED_HOST.sub(
                        self.UPLOAD_URL, response.urljoin(link.attrib["href"])
                    )
                ],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )

    def parse_editions(self, response):
        links = response.css('a[href*="/diario-oficial-eletronico-"]')
        for link, gazette_date, is_extra_edition in self._dated_links(links):
            yield response.follow(
                link,
                callback=self.parse_gazette_page,
                cb_kwargs={
                    "gazette_date": gazette_date,
                    "is_extra_edition": is_extra_edition,
                },
            )

    def parse_gazette_page(self, response, gazette_date, is_extra_edition):
        # The PDF is only reachable through a JS redirect on the edition page
        gazette_url = response.xpath("//script/text()").re_first(
            r"window\.location\s*=\s*[\"']([^\"']+\.pdf)"
        )
        if gazette_url is None:
            self.logger.warning(f"PDF URL not found in {response.url}")
            return

        yield Gazette(
            date=gazette_date,
            file_urls=[response.urljoin(gazette_url)],
            is_extra_edition=is_extra_edition,
            power="executive_legislative",
        )

    def _dated_links(self, links):
        for link in links:
            text = link.xpath("string()").get()
            href = unquote(link.attrib["href"])
            # The displayed date wins: some filenames carry the upload date
            gazette_date = self._parse_date(text) or self._parse_date(href)
            if gazette_date is None:
                self.logger.warning(f"Date not found in {href}")
                continue

            if self.start_date <= gazette_date <= self.end_date:
                is_extra_edition = bool(
                    self.EXTRA_EDITION.search(f"{text} {href}".upper())
                )
                yield link, gazette_date, is_extra_edition

    def _parse_date(self, value):
        for pattern, date_format in self.DATE_PATTERNS:
            match = pattern.search(value)
            if match is None:
                continue
            try:
                raw_date = "".join(match.groups())
                return datetime.strptime(raw_date, date_format).date()
            except ValueError:
                continue
        return None
