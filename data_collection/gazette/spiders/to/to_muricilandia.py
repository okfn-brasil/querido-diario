from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToMuricilandiaSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1713957"
    name = "to_muricilandia"
    BASE_URL = "https://muricilandia.diariooficialbr.com.br"
    start_date = date(2019, 7, 2)
