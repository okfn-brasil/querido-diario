from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbRiachaoSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2512747"
    name = "pb_riachao"
    allowed_domains = ["riachao.pb.gov.br"]
    BASE_URL = "https://www.riachao.pb.gov.br"
    start_date = date(2024, 2, 29)
