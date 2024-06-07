from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToMiracemaSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "3303005"
    name = "to_miracema"
    allowed_domains = ["diariooficialbr.com.br"]
    BASE_URL = "https://miracema.diariooficialbr.com.br"
    start_date = date(2020, 11, 27)
