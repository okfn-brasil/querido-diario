from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaBomLugarSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2102077"
    name = "ma_bom_lugar"
    allowed_domains = ["bomlugar.ma.gov.br"]
    BASE_URL = "https://www.bomlugar.ma.gov.br"
    start_date = date(2013, 1, 13)
