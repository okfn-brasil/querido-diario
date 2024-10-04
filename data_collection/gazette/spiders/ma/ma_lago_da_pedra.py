from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaLagoDaPedraSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2105708"
    name = "ma_lago_da_pedra"
    allowed_domains = ["lagodapedra.ma.gov.br"]
    BASE_URL = "https://www.lagodapedra.ma.gov.br"
    start_date = date(2018, 12, 31)
