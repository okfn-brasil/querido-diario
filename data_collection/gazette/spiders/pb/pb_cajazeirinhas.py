from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCajazeirinhasSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2503753"
    name = "pb_cajazeirinhas"
    allowed_domains = ["cajazeirinhas.pb.gov.br"]
    BASE_URL = "https://www.cajazeirinhas.pb.gov.br"
    start_date = date(2024, 2, 6)
