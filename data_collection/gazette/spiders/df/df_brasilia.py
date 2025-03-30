import datetime
from urllib.parse import parse_qs, urlparse

from dateparser import parse
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider
from gazette.utils.dates import monthly_sequence

MONTH_MAP = {
    idx + 1: value
    for idx, value in enumerate(
        [
            "01_Janeiro",
            "02_Fevereiro",
            "03_Março",
            "04_Abril",
            "05_Maio",
            "06_Junho",
            "07_Julho",
            "08_Agosto",
            "09_Setembro",
            "10_Outubro",
            "11_Novembro",
            "12_Dezembro",
        ]
    )
}


class DfBrasiliaSpider(BaseGazetteSpider):
    TERRITORY_ID = "5300108"
    name = "df_brasilia"
    allowed_domains = ["dodf.df.gov.br"]
    start_date = datetime.date(1967, 12, 25)

    BASE_URL = "https://dodf.df.gov.br"

    def start_requests(self):
        for date in monthly_sequence(self.start_date, self.end_date):
            month_value = MONTH_MAP.get(date.month)
            yield Request(
                f"{self.BASE_URL}/dodf/jornal/pastas?pasta={date.year}/{month_value}",
                callback=self.parse_month,
            )

    def parse_month(self, response):
        """Parses available dates to request a list of documents for each date."""
        gazette_days_url = response.css(".lista-arquivos a::attr(href)").getall()

        for url in gazette_days_url:
            date = url.split("/")[-1]
            date = parse(date, settings={"DATE_ORDER": "DMY"}).date()

            if self.start_date <= date <= self.end_date:
                yield Request(
                    urlparse(url)._replace(scheme="https").geturl(),
                    callback=self.parse_gazette,
                    cb_kwargs={"date": date},
                )

    def parse_gazette(self, response, date):
        """Parses list of documents to request each one for the date."""
        gazette_editions = response.css(".lista-arquivos a::attr(href)").getall()

        if not gazette_editions:
            return

        for url_edition in gazette_editions:
            gazette_name = parse_qs(urlparse(url_edition).query)["arquivo"][0]
            edition_number = gazette_name.split()[1]
            is_extra_edition = "extra" in gazette_name.lower()
            gazette_url = f"{self.BASE_URL}{url_edition}"

            yield Gazette(
                date=date,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                power="executive",
                file_urls=[gazette_url],
            )
