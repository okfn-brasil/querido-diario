from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbJacarauSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2507309"
    name = "pb_jacarau"
    allowed_domains = ["jacarau.pb.gov.br"]
    BASE_URL = "https://www.jacarau.pb.gov.br"
    start_date = date(2019, 3, 7)
