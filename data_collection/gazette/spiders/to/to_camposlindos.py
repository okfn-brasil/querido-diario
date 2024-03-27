import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToCamposLindosSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1703842"
    name = "to_campos_lindos"
    allowed_domains = ["camposlindos.diariooficialbr.com.br"]
    start_date = datetime.date(2021, 4, 30)
    BASE_URL = "https://camposlindos.diariooficialbr.com.br"
