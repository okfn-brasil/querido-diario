from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbSerrariaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2515906"
    name = "pb_serraria"
    allowed_domains = ["serraria.pb.gov.br"]
    BASE_URL = "https://www.serraria.pb.gov.br"
    start_date = date(2024, 3, 1)
