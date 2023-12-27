import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficinalBRSpider


class ToGoiatinsSpider(BaseDiarioOficinalBRSpider):
    TERRITORY_ID = "1709005"
    name = "to_goiatins"
    allowed_domains = ["goiatins.diariooficialbr.com.br"]
    start_date = datetime.date(2021, 1, 14)
    city_domain = "goiatins.diariooficialbr.com.br"
    url_base = "https://goiatins.diariooficialbr.com.br"
