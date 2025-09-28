from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class CePacajusSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2309607"
    name = "ce_pacajus"
    allowed_domains = ["pacajus.ce.gov.br"]
    BASE_URL = "https://www.pacajus.ce.gov.br"
    start_date = date(2018, 10, 26)
