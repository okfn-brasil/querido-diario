from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbJericoSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2507408"
    name = "pb_jerico"
    allowed_domains = ["jerico.pb.gov.br"]
    BASE_URL = "https://www.jerico.pb.gov.br"
    start_date = date(2021, 6, 1)
