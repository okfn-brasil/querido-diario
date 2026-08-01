from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class RnPauDosFerrosSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2409407"
    name = "rn_pau_dos_ferros_2022"
    allowed_domains = ["paudosferros.rn.gov.br"]
    BASE_URL = "https://www.paudosferros.rn.gov.br"
    start_date = date(2022, 9, 28)
