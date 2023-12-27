import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficinalBRSpider


class ToPeixeSpider(BaseDiarioOficinalBRSpider):
    TERRITORY_ID = "1716604"
    name = "to_peixe"
    allowed_domains = ["peixe.diariooficialbr.com.br"]
    start_date = datetime.date(2022, 3, 30)
    city_domain = "peixe.diariooficialbr.com.br"
    url_base = "https://peixe.diariooficialbr.com.br"
