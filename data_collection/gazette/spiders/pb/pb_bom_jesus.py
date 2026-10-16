from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbBomJesusSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2502201"
    name = "pb_bom_jesus"
    allowed_domains = ["prefeiturabomjesus.pb.gov.br"]
    BASE_URL = "https://www.prefeiturabomjesus.pb.gov.br"
    start_date = date(14, 2, 10)
