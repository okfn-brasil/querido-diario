from datetime import date
from time import sleep
from gazette.spiders.base import BaseGazetteSpider
from gazette.items import Gazette


class SpUbatubaSpider(BaseGazetteSpider):
    name = "sp_ubatuba"
    allowed_domains = ["https://www.ubatuba.sp.gov.br"]
    start_urls = ["https://www.ubatuba.sp.gov.br/wp-content/plugins/pmu-diariooficial/archive-diariooficial.sql.1.10"
                  ".7.php"]
    TERRITORY_ID = "3555406"
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
    }

    def parse(self, response):
        gazettes = response.json()['data']
        for gazette in gazettes:
            date = self.extract_date(gazette[2])
            url = self.extract_url(gazette[1])
            edition_number = self.extract_edition_number(gazette[1])
            yield Gazette(
                date=date,
                edition_number=edition_number,
                file_urls=[url],
                power="executive")

    @staticmethod
    def extract_date(date_item):
        date_string = date_item.split('>')[1].split('<')[0]
        data_int = [int(item) for item in date_string.split('/')]
        return date(int(data_int[2]), int(data_int[1]), int(data_int[0]))

    def extract_url(self, url_item):
        return self.allowed_domains[0] + url_item.split("href=\"")[1].split("\"")[0]

    @staticmethod
    def extract_edition_number(edition_item):
        return edition_item.split('>')[1].split('<')[0]





