from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaVargemGrandeSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2112704"
    name = "ma_vargem_grande"
    allowed_domains = ["vargemgrande.ma.gov.br"]
    BASE_URL = "https://www.vargemgrande.ma.gov.br"
    start_date = date(2017, 1, 8)
