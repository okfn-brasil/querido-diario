from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToPeixeSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1716604"
    name = "to_peixe"
    allowed_domains = ["diariooficialbr.com.br"]
    BASE_URL = "https://peixe.diariooficialbr.com.br"
    start_date = date(2022, 3, 30)
