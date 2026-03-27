import re
import urllib
from datetime import date, timedelta

import dateparser
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import yearly_sequence


class MgMontesClarosSpider(BaseGazetteSpider):
    TERRITORY_ID = "3143302"
    name = "mg_montes_claros"
    allowed_domains = ["diariooficial.montesclaros.mg.gov.br"]
    base_url = "https://diariooficial.montesclaros.mg.gov.br"
    start_date = date(2013, 7, 2)

    PDFLINK_REGEX = re.compile(r"^.*(http(s?)://[^']+\.pdf).*$", re.IGNORECASE)
    EXTRA_EDITION_MARK = "EDIÇÃO EXTRA"
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
        for year in yearly_sequence(self.start_date, self.end_date):
            if year > 2017:
                yield Request(
                    f"{self.base_url}/exercicio-{year}",
                    callback=self.parse_new_format,
                )
            elif year == 2017 or year == 2016:
                for month in range(12):
                    month_begin = date(year, month + 1, 1)
                    if month_begin < self.start_date:
                        continue

                    end_month = (month_begin + timedelta(days=32)).replace(day=1)
                    if end_month > self.end_date:
                        continue

                    yield Request(
                        f"{self.base_url}/{year}/{self.MONTHS[month]}",
                        callback=self.parse_old_format,
                    )
            else:
                yield Request(
                    f"{self.base_url}/{year}/edicoes-de-{year}",
                    callback=self.parse_old_format,
                )

    def _get_date_from_link(self, link):
        link_date = link.re_first("([0-9]{2}-[0-9]{2}-[0-9]{2})")
        if not link_date:
            link_date = link.re_first("([0-9]{2}/[0-9]{2}/[0-9]{4})")
            if not link_date:
                link_date = link.re_first("([0-9]{2}[0-9]{2}[0-9]{4})")
                if not link_date:
                    # Url tem um erro no nome do pdf (202 ao invés de 2022)
                    if re.match(
                        "diario-oficial-eletronico-0510202",
                        link.xpath("@href").extract_first(),
                    ):
                        link_date = "05 10 2022"
                    else:
                        return None
                link_date = f"{link_date[0:2]} {link_date[2:4]} {link_date[4:]}"
        gazette_date = dateparser.parse(link_date, settings={"DATE_ORDER": "DMY"})

        if gazette_date is None:
            # could not parse date for some reason. When this was written this condition
            # was not triggered
            return None

        gazette_date = gazette_date.date()
        return gazette_date

    def parse_new_format(self, response):
        links = response.xpath('//a[contains(@href, "diario-oficial-eletronico")]')

        for link in links:
            title = link.css("*::text").extract_first()
            url = link.xpath("@href").extract_first()

            # Lista de convocados de um concurso, não é relevante
            if "lista-unica-classificacao-definitiva-pcd-ps01" in url:
                continue

            gazette_date = self._get_date_from_link(link)

            if (
                gazette_date is None
                or gazette_date > self.end_date
                or gazette_date < self.start_date
            ):
                continue

            is_extra_edition = self.EXTRA_EDITION_MARK in title.upper()

            yield Request(
                url=url,
                callback=self.get_pdf_from_window_hook,
                cb_kwargs={
                    "gazette_date": gazette_date,
                    "is_extra_edition": is_extra_edition,
                },
            )

    def get_pdf_from_window_hook(self, response, gazette_date, is_extra_edition):
        """
        On the new format the link in the list is to a page that loads the pdf file through a js
        hook on the page load. This second request extracts the actual pdf file.
        """
        js = response.xpath("//script").extract_first()
        match = self.PDFLINK_REGEX.match(js)
        if not match:
            return None

        link = match.group(1)
        return Gazette(
            date=gazette_date,
            file_urls=[link],
            is_extra_edition=is_extra_edition,
            power="executive_legislative",
        )

    def parse_old_format(self, response):
        links = response.xpath(
            '//a[contains(@href, "%s")]'
            % (urllib.parse.quote("Diário Oficial Eletrônico"))
        )

        for link in links:
            title = link.css("*::text").extract_first()
            url = link.xpath("@href").extract_first()

            gazette_date = self._get_date_from_link(link)
            if (
                gazette_date is None
                or gazette_date > self.end_date
                or gazette_date < self.start_date
            ):
                continue

            is_extra_edition = self.EXTRA_EDITION_MARK in title.upper()

            yield Gazette(
                date=gazette_date,
                file_urls=[url],
                is_extra_edition=is_extra_edition,
                power="executive_legislative",
            )
