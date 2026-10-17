from datetime import date

from gazette.spiders.base.dosp import BaseDospSpider


class SpAvaiSpider(BaseDospSpider):
    TERRITORY_ID = "3504305"
    name = "sp_avai"
    start_urls = ["https://www.imprensaoficialmunicipal.com.br/avai"]
    start_date = date(2017, 9, 18)
