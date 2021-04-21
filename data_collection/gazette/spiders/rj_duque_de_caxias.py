import scrapy

from datetime import date

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjDuqueDeCaxiasSpider(BaseGazetteSpider):
    
    TERRITORY_ID = "3301702"
    name = "rj_duque_de_caxias"
    allowed_domains = ["duquedecaxias.rj.gov.br"]
    start_urls = ["https://duquedecaxias.rj.gov.br"]
    base_url_before_2017 = "https://duquedecaxias.rj.gov.br/portal/arquivos/{}/{}/"
    base_url_after_2017 = "https://duquedecaxias.rj.gov.br/portal/{}.html"
    start_date = date(2013, 1, 1)

    month_names = [
        "Janeiro",
        "Fevereiro",
        "Marco",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]


    def start_requests(self):
        end_date = date.today()
        year = self.start_date.year
        while year <= end_date.year:
            month = self.start_date.month
            while month <= len(self.month_names):
                if year < 2017:
                    folder_month_name = "{:02d}".format(month + 1) + "-" + self.month_names[month]
                    url = self.base_url_before_2017.format(year, folder_month_name, " ")
                else:
                    url = self.base_url_after_2017.format(year)
                yield scrapy.Request(url)
                month += 1
            year += 1

    def parse(self, response):
