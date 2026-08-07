from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCapimSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2504033"
    name = "pb_capim"
    allowed_domains = ["capim.pb.gov.br"]
    BASE_URL = "https://www.capim.pb.gov.br"
    start_date = date(2023, 9, 11)
