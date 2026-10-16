from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbAlagoaNovaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2500403"
    name = "pb_alagoa_nova"
    allowed_domains = ["alagoanova.pb.gov.br"]
    BASE_URL = "https://www.alagoanova.pb.gov.br"
    start_date = date(2024, 1, 9)
