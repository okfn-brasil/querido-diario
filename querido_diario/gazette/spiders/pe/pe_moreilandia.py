from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PeMoreilandiaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2614303"
    name = "pe_moreilandia"
    allowed_domains = ["moreilandia.pe.gov.br"]
    BASE_URL = "https://www.moreilandia.pe.gov.br"
    start_date = date(2021, 4, 9)
