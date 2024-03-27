import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToPeixeSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1716604"
    name = "to_peixe"
    allowed_domains = ["peixe.diariooficialbr.com.br"]
    start_date = datetime.date(2022, 3, 30)
    BASE_URL = "https://peixe.diariooficialbr.com.br"
