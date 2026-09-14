import datetime as dt
import re

from scrapy import Request
from w3lib.url import add_or_replace_parameter

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence


class RsPortoAlegreSpider(BaseGazetteSpider):
    TERRITORY_ID = "4314902"
    name = "rs_porto_alegre"
    allowed_domains = [
        "apigateway.procempa.com.br",
        "atom2.procempa.com.br",
    ]
    start_date = dt.date(1995, 3, 15)

    ARCHIVE_START_DATE = dt.date(1995, 3, 15)
    ARCHIVE_END_DATE = dt.date(2011, 4, 29)
    API_START_DATE = dt.date(2011, 5, 2)

    ARCHIVE_YEAR_URL = (
        "https://atom2.procempa.com.br/index.php/"
        "diario-oficial-de-porto-alegre-de-{year}"
    )

    ARCHIVE_YEAR_URL_OVERRIDES = {
        2003: (
            "https://atom2.procempa.com.br/index.php/"
            "diario-oficial-de-porto-alegre-de-2003-2"
        ),
    }
    API_BASE_URL = (
        "https://apigateway.procempa.com.br/apiman-gateway/"
        "administracao-planejamento/dopa/1.1"
    )

    ARCHIVE_TITLE_PATTERN = re.compile(
        r"DOPA\s+(?:(?:\d+ª\s+)?edição(?:\s+extra)?\s+)?"
        r"N[º°.]?\s*([\d.]+)\s+de\s+(\d{2}/\d{2}/\d{4})",
        re.IGNORECASE,
    )

    custom_settings = {"CONCURRENT_REQUESTS": 8}

    def __api_start_date(self):
        return max(self.start_date, self.API_START_DATE)

    async def start(self):
        archive_start = max(self.start_date, self.ARCHIVE_START_DATE)
        archive_end = min(self.end_date, self.ARCHIVE_END_DATE)

        if archive_start <= archive_end:
            for year in range(archive_start.year, archive_end.year + 1):
                period_start = max(archive_start, dt.date(year, 1, 1))
                period_end = min(archive_end, dt.date(year, 12, 31))
                archive_url = self.ARCHIVE_YEAR_URL_OVERRIDES.get(
                    year, self.ARCHIVE_YEAR_URL.format(year=year)
                )
                yield Request(
                    archive_url,
                    callback=self.parse_archive_year,
                    cb_kwargs={
                        "period_start": period_start,
                        "period_end": period_end,
                    },
                )

        api_start = self.__api_start_date()
        if api_start <= self.end_date:
            for month_date in monthly_sequence(api_start, self.end_date):
                url = (
                    f"{self.API_BASE_URL}/api/diarios/busca-por-mes-agrupada"
                    f"?mes={month_date.month}&ano={month_date.year}"
                )
                yield Request(url, callback=self.parse_api_month)

    def parse_archive_year(self, response, period_start, period_end):
        browse_url = response.xpath(
            '//a[contains(normalize-space(.), "Exibir tudo")]/@href'
        ).get()

        if not browse_url:
            self.logger.warning(
                "Archive year page %s does not expose the full listing.",
                response.url,
            )
            return

        browse_url = add_or_replace_parameter(
            response.urljoin(browse_url), "view", "table"
        )

        yield response.follow(
            browse_url,
            callback=self.parse_archive_list,
            cb_kwargs={
                "period_start": period_start,
                "period_end": period_end,
            },
        )

    def parse_archive_list(self, response, period_start, period_end):
        edition_links = response.xpath('//a[contains(normalize-space(.), "DOPA")]')

        for edition_link in edition_links:
            title = " ".join(edition_link.xpath(".//text()").getall()).strip()
            metadata = self._extract_archive_metadata(title)
            if metadata is None:
                continue

            date, edition_number, is_extra_edition = metadata
            if not period_start <= date <= period_end:
                continue

            yield response.follow(
                edition_link,
                callback=self.parse_archive_item,
                cb_kwargs={
                    "date": date,
                    "edition_number": edition_number,
                    "is_extra_edition": is_extra_edition,
                },
            )

        next_page = response.xpath('//a[normalize-space(.)="Próximo"]/@href').get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse_archive_list,
                cb_kwargs={
                    "period_start": period_start,
                    "period_end": period_end,
                },
            )

    def parse_archive_item(
        self,
        response,
        date,
        edition_number,
        is_extra_edition,
    ):
        file_url = response.css('a[href$=".pdf"]::attr(href)').get()
        if not file_url:
            self.logger.warning(
                "Archive edition %s from %s does not have a PDF link.",
                edition_number,
                date,
            )
            return

        yield Gazette(
            date=date,
            edition_number=edition_number,
            file_urls=[response.urljoin(file_url)],
            is_extra_edition=is_extra_edition,
            power="executive_legislative",
        )

    def _extract_archive_metadata(self, title):
        match = self.ARCHIVE_TITLE_PATTERN.search(title)
        if not match:
            self.logger.warning("Unable to parse archive edition title: %s", title)
            return None

        edition_number = int(match.group(1).replace(".", ""))
        date = dt.datetime.strptime(match.group(2), "%d/%m/%Y").date()
        is_extra_edition = "extra" in title.lower()

        return date, edition_number, is_extra_edition

    def parse_api_month(self, response):
        gazettes_by_power = response.json()
        api_start = self.__api_start_date()

        for api_power, power in (
            ("executivo", "executive"),
            ("legislativo", "legislative"),
        ):
            for date_group in gazettes_by_power.get(api_power, []):
                raw_date = date_group.get("data")
                if not raw_date:
                    self.logger.warning(
                        "Date group for power %s does not have a date.", api_power
                    )
                    continue

                try:
                    date = dt.datetime.strptime(raw_date, "%d/%m/%Y").date()
                except (TypeError, ValueError):
                    self.logger.warning(
                        "Unable to parse date %r for power %s.", raw_date, api_power
                    )
                    continue

                if not api_start <= date <= self.end_date:
                    continue

                for publication in date_group.get("publicacoes", []):
                    edition_number = publication.get("numeroEdicao")
                    is_extra_edition = publication.get("isExtra")
                    link_download = publication.get("linkDownload")

                    if edition_number is None:
                        self.logger.warning(
                            "Publication %s does not have an edition number.",
                            publication.get("idEdicao"),
                        )
                        continue

                    if is_extra_edition is None:
                        self.logger.warning(
                            "Publication %s does not have an isExtra flag.",
                            publication.get("idEdicao"),
                        )
                        continue

                    if not link_download:
                        self.logger.warning(
                            "Edition %s does not have a download link.",
                            publication.get("idEdicao"),
                        )
                        continue

                    if link_download.startswith(("http://", "https://")):
                        file_url = link_download
                    else:
                        file_url = f"{self.API_BASE_URL}/{link_download.lstrip('/')}"

                    yield Gazette(
                        date=date,
                        edition_number=edition_number,
                        file_urls=[file_url],
                        is_extra_edition=is_extra_edition,
                        power=power,
                    )
