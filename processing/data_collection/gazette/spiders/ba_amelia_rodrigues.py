from datetime import date, datetime
from gazette.spiders.base import BaseGazetteSpider
import scrapy


def get_next_month(current_date):
    # https://stackoverflow.com/a/22236549
    month = (current_date.month % 12) + 1
    year = current_date.year + (current_date.month + 1 > 12)
    return date(year, month, 1)


class BaAmeliaRodriguesSpider(BaseGazetteSpider):

    name = "ba_amelia_rodrigues"
    allowed_domains = ["pmameliarodriguesba.imprensaoficial.org"]
    start_date = date(2015, 1, 1)

    TERRITORY_ID = "2901106"

    def start_requests(self):
        """Gera as requests as páginas dos Diários."""
        current_date = self.start_date
        while current_date <= date.today():
            year_month = current_date.strftime("%Y/%m")  # like 2015/01
            # format http://pmameliarodriguesba.imprensaoficial.org/2015/01/
            url = f"http://pmameliarodriguesba.imprensaoficial.org/{year_month}/"
            current_date = get_next_month(current_date)
            yield scrapy.Request(url, callback=self.extract_gazette_links)

    def extract_gazette_links(self, response):
        # FIXME add pagination
        for a in response.css("h2 a"):
            yield scrapy.Request(a.attrib["href"], callback=self.parse)

    def parse(self, response):
        pass
