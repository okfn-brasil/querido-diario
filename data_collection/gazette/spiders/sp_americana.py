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
    start_urls = ["https://diariooficial.americana.sp.gov.br/diario-oficial-edicaoAnterior.php"]
    extra_editions = "https://diariooficial.americana.sp.gov.br/diario-oficial-edicaoExtra.php"

    locations = {
        "gazette": "//*[@class='day table-light']/strong/a",
        "extra_gazette_url": "//*[@class='list-group-item']/a/@href",
        "extra_gazette_date": "//*[@class='list-group-item']/text()"}

    def parse(self, response):

        param_url = f"?mes={self.start_date.month}&ano={self.start_date.year}"
        base_url = response.url
        url = base_url + param_url
        date = self.start_date

        while date.year < datetime.date.today().year or date.month < datetime.date.today().month:
            yield response.follow(url, self.parse_gazette)
            date = date + relativedelta(months=+1)
            url = base_url + f"?mes={date.month}&ano={date.year}"

        yield response.follow(self.extra_editions, self.extra_parse_gazette)

    def parse_gazette(self, response):

        gazettes = response.xpath(self.locations["gazette"]).extract()
        for gazette in gazettes:
            file_url = gazette.split('"')[1]
            date = gazette.split('"')[7][6:16]
            date = dateparser.parse(date, date_formats=["%d/%m/%Y"]).date()
            edition = re.findall(r'\d+', gazette.split(';')[2])[0]

            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=False,
                power="executive",
                edition_number=edition,

            )

    def extra_parse_gazette(self, response):

        gazettes = response.xpath(self.locations['extra_gazette_url']).extract()
        dates = response.xpath(self.locations['extra_gazette_date']).extract()[2::3]
        counter = 0
        while counter < len(gazettes):
            file_url = gazettes[counter]
            date = dateparser.parse(dates[counter][2:12], date_formats=["%d/%m/%Y"]).date()
            counter += 1
            yield Gazette(
                date=date,
                file_urls=[file_url],
                is_extra_edition=True,
                power="executive",
            )
