from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnTaboleiroGrandeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2413805"
    name = "rn_taboleiro_grande"
    allowed_domains = ["taboleirogrande.rn.gov.br"]
    BASE_URL = "https://www.taboleirogrande.rn.gov.br"
    start_date = date(2013, 1, 28)
