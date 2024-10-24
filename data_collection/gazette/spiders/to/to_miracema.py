from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToMiracemaSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1713205"
    name = "to_miracema"
    allowed_domains = ["miracema.diariooficialbr.com.br"]
    BASE_URL = "https://miracema.diariooficialbr.com.br"
    start_date = date(2023, 1, 16)
