from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbMarizopolisSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2509156"
    name = "pb_marizopolis"
    allowed_domains = ["marizopolis.pb.gov.br"]
    BASE_URL = "https://www.marizopolis.pb.gov.br"
    start_date = date(2021, 1, 27)
