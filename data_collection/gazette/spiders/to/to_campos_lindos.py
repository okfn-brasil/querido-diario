from datetime import date

from gazette.spiders.base.diariooficialbr import BaseDiarioOficialBRSpider


class ToCamposLindosSpider(BaseDiarioOficialBRSpider):
    TERRITORY_ID = "1703842"
    name = "to_campos_lindos"
    BASE_URL = "https://camposlindos.diariooficialbr.com.br"
    start_date = date(2021, 5, 31)
