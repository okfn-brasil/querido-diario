from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToGoiatinsSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1709005"
    name = "to_goiatins"
    BASE_URL = "https://goiatins.diariooficialbr.com.br"
    start_date = date(2021, 1, 14)
