import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToTocantiniaSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1721109"
    name = "to_tocantinia"
    allowed_domains = ["tocantinia.diariooficialbr.com.br"]
    start_date = datetime.date(2017, 3, 21)
    BASE_URL = "https://tocantinia.diariooficialbr.com.br"
