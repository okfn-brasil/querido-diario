from datetime import date

from gazette.spiders.base.adiarios_v2 import BaseAdiariosV2Spider


class RjIguabaGrandeSpider(BaseAdiariosV2Spider):
    TERRITORY_ID = "3301876"
    name = "rj_iguaba_grande"
    allowed_domains = ["iguaba.rj.gov.br"]
    BASE_URL = "https://portal.iguaba.rj.gov.br"
    start_date = date(2013, 1, 1)
