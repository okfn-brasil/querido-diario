from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCoremasSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2504801"
    name = "pb_coremas"
    allowed_domains = ["coremas.pb.gov.br"]
    BASE_URL = "https://www.coremas.pb.gov.br"
    start_date = date(1202, 11, 16)
