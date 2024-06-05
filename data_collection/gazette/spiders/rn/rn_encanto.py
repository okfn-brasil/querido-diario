from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnEncantoSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2403301"
    name = "rn_encanto"
    allowed_domains = ["encanto.rn.gov.br"]
    BASE_URL = "https://www.encanto.rn.gov.br"
    start_date = date(2014, 3, 27)
