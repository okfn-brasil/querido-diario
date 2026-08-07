from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnFranciscoDantasSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2403905"
    name = "rn_francisco_dantas"
    allowed_domains = ["franciscodantas.rn.gov.br"]
    BASE_URL = "https://www.franciscodantas.rn.gov.br"
    start_date = date(1983, 5, 5)
