import dateparser
from scrapy import Spider
import datetime
from dateutil.relativedelta import relativedelta
from gazette.items import Gazette
import re


class SpAmericanaSpider(Spider):
    TERRITORY_ID = "3501608"
    name = "sp_americana"
    allowed_domains = ["diariooficial.americana.sp.gov.br"]
    start_date = datetime.date(2018, 9, 1)  # First gazette available
    start_urls = [
        "https://diariooficial.americana.sp.gov.br/diario-oficial-edicaoAnterior.php"
    ]
    extra_editions = (
        "https://diariooficial.americana.sp.gov.br/diario-oficial-edicaoExtra.php"
    )

    locations = {
        "gazette": ".day a",
        "gazette_details": "::attr(title)",
        "gazette_url": "::attr(href)",
        "extra_gazette": "li.list-group-item",
    }

    def parse(self, response):

        param_url = f"?mes={self.start_date.month}&ano={self.start_date.year}"
        base_url = response.url
        url = base_url + param_url
        date = self.start_date
        today = datetime.date.today()

        while (
            date.year < today.year
            or date.month < today.month
        ):
            yield response.follow(url, self.parse_gazette)
            date = date + relativedelta(months=+1)
            url = base_url + f"?mes={date.month}&ano={date.year}"

        yield response.follow(self.extra_editions, self.extra_parse_gazette)

    def parse_gazette(self, response):

        gazettes = response.css(self.locations["gazette"])

        for gazette in gazettes:

            file_url = gazette.css(self.locations["gazette_url"]).get()
            details = gazette.css(self.locations["gazette_details"])
            date = details.re_first(r"(\d{2}\/\d{2}\/\d{4})")
            date = dateparser.parse(date, date_formats=["%d/%m/%Y"]).date()
            edition = details.re_first("No:\s*(\d+)")

            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=False,
                power="executive",
                edition_number=edition,
            )

    def extra_parse_gazette(self, response):

        gazettes = response.css(self.locations["extra_gazette"])

        for gazette in gazettes:

            file_url = gazette.css(self.locations["gazette_url"]).get()
            date = gazette.re_first(r"(\d{2}\/\d{2}\/\d{4})")
            date = dateparser.parse(
                date, date_formats=["%d/%m/%Y"]
            ).date()
            edition = gazette.re_first("\d{3}")
            
            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=True,
                power="executive",
                edition_number=edition,
            )
