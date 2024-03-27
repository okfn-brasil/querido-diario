import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToGoiatinsSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1709005"
    name = "to_goiatins"
    allowed_domains = ["goiatins.diariooficialbr.com.br"]
    start_date = datetime.date(2021, 1, 14)
    BASE_URL = "https://goiatins.diariooficialbr.com.br"
