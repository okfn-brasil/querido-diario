from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class MaVilaNovaDosMartiriosSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2112852"
    name = "ma_vila_nova_dos_martirios"
    allowed_domains = ["vilanovadosmartirios.ma.gov.br"]
    BASE_URL = "https://www.vilanovadosmartirios.ma.gov.br"
    start_date = date(2021, 6, 14)
