import datetime

from gazette.spiders.base.diariooficialbr import BaseDiarioOficinalBRSpider


class ToCamposLindosSpider(BaseDiarioOficinalBRSpider):
    TERRITORY_ID = "1703842"
    name = "to_camposlindos"
    allowed_domains = ["camposlindos.diariooficialbr.com.br"]
    start_date = datetime.date(2021, 4, 30)
    city_domain = "camposlindos.diariooficialbr.com.br"
    url_base = "https://camposlindos.diariooficialbr.com.br"
