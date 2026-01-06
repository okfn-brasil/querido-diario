from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbSertaozinhoSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2515930"
    name = "pb_sertaozinho"
    allowed_domains = ["sertaozinho.pb.gov.br"]
    BASE_URL = "https://www.sertaozinho.pb.gov.br"
    start_date = date(2024, 2, 1)
