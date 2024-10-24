from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToTalismaSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1720978"
    name = "to_talisma"
    allowed_domains = ["talisma.diariooficialbr.com.br"]
    BASE_URL = "https://talisma.diariooficialbr.com.br"
    start_date = date(2020, 1, 2)
