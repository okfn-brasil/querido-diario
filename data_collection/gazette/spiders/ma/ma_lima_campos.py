from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaLimaCamposSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2106003"
    name = "ma_lima_campos"
    allowed_domains = ["limacampos.ma.gov.br"]
    BASE_URL = "https://www.limacampos.ma.gov.br"
    start_date = date(2013, 1, 2)
