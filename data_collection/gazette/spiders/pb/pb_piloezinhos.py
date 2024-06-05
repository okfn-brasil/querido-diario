from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbPiloezinhosSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2511707"
    name = "pb_piloezinhos"
    allowed_domains = ["piloezinhos.pb.gov.br"]
    BASE_URL = "https://www.piloezinhos.pb.gov.br"
    start_date = date(2022, 6, 1)
