from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnRodolfoFernandesSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2411007"
    name = "rn_rodolfo_fernandes"
    allowed_domains = ["rodolfofernandes.rn.gov.br"]
    BASE_URL = "https://www.rodolfofernandes.rn.gov.br"
    start_date = date(2015, 2, 5)
