from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaBomJardimSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2102002"
    name = "ma_bom_jardim"
    allowed_domains = ["bomjardim.ma.gov.br"]
    BASE_URL = "https://www.bomjardim.ma.gov.br"
    start_date = date(2017, 7, 19)
