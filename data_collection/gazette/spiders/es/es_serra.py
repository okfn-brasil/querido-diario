from datetime import date

from gazette.spiders.base.dionet import BaseDionetSpider


class EsSerraSpider(BaseDionetSpider):
    TERRITORY_ID = "3205002"
    name = "es_serra"
    allowed_domains = ["ioes.dio.es.gov.br"]
    start_date = date(2021, 1, 1)

    BASE_URL = "https://ioes.dio.es.gov.br"
    url_subtheme = "?subtheme=diariodaserra"
