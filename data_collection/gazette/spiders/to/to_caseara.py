from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToCasearaSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1703909"
    name = "to_caseara"
    allowed_domains = ["caseara.diariooficialbr.com.br"]
    BASE_URL = "https://caseara.diariooficialbr.com.br"
    start_date = date(2019, 6, 26)
