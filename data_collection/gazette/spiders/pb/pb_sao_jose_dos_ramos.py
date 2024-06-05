from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbSaoJoseDosRamosSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2514453"
    name = "pb_sao_jose_dos_ramos"
    allowed_domains = ["saojosedosramos.pb.gov.br"]
    BASE_URL = "https://www.saojosedosramos.pb.gov.br"
    start_date = date(2021, 1, 4)
