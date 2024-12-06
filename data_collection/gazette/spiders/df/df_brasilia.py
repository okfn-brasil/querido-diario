import datetime
import re

from dateparser import parse
from dateutil.rrule import MONTHLY, rrule
import dateutil.parser
from urllib.parse import urlparse,parse_qs,unquote
from scrapy import Request

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

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
    zyte_smartproxy_enabled = True

    TERRITORY_ID = "5300108"
    name = "df_brasilia"
    allowed_domains = ["dodf.df.gov.br"]
    start_date = datetime.date(1967, 12, 25)
    
    BASE_URL = "https://dodf.df.gov.br/dodf/jornal/pastas"

    def start_requests(self):
        months_by_year = [
            (date.month, date.year)
            for date in rrule(
                MONTHLY, dtstart=self.start_date.replace(day=1), until=self.end_date
            )
        ]
        for month, year in months_by_year:
            month_value = MONTH_MAP.get(month)
            yield Request(
                f"{self.BASE_URL}?pasta={year}/{month_value}",
                meta={"month": month_value, "year": year},
                callback=self.parse_month,
            )

    def parse_month(self, response):
        """Parses available dates to request a list of documents for each date."""
        month, year = response.meta["month"], response.meta["year"]
        gazette_days = response.css(".lista-arquivos a::attr(href)").getall()
        for url in gazette_days:
            date = unquote(url.split('/')[-1])

            if date is None:
                continue

            try:
                date_parsed = dateutil.parser.parse(date, dayfirst=True).date() #.strftime('%d-%m-%Y') 
                valid_date = True
            except dateutil.parser._parser.ParserError as ex:
                date_parsed = ex
                valid_date = False

            if valid_date:
                date = parse(date, settings={"DATE_ORDER": "DMY"}).date()

                if date < self.start_date:
                    continue

                yield Request(url, meta={"date_route":date_parsed}, callback=self.parse_gazette)

    def parse_gazette(self, response):
        """Parses list of documents to request each one for the date."""
        DATE_REGEX = r"[0-9]{2}-[0-9]{2}[ -][0-9]{2,4}"
        PDF_URL = "https://dodf.df.gov.br/dodf/jornal/visualizar-pdf?{}"
        
        gazette_editions = response.css(".lista-arquivos a::attr(href)").getall()
        if not gazette_editions:
            self.logger.warning(f"Document not found in {response.url}")
            return

        for url_edition in gazette_editions:
            query_edition = urlparse(url_edition).query
            pdfname = parse_qs(query_edition)['arquivo'][0]
            try:
                date_pdfname = re.search(DATE_REGEX, pdfname).group()
                date_parsed = parse(date_pdfname, settings={"DATE_ORDER": "DMY"}).date()
            except:
                date_parsed = response.meta["date_route"]

            edition_number = [chunck for chunck in pdfname.split(' ') if chunck.isnumeric()][0]
            is_extra_edition = "EXTRA" in pdfname
            is_supplement_edition = "SUPLEMENTO" in pdfname
            file_urls = [PDF_URL.format(query_edition)]


            yield Gazette(
                date=date_parsed,
                edition_number=edition_number,
                is_extra_edition=is_extra_edition,
                s_supplement_edition=s_supplement_edition,
                power="executive",
                file_urls=file_urls
            )
