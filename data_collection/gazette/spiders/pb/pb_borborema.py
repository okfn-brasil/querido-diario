from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbBorboremaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2502706"
    name = "pb_borborema"
    allowed_domains = ["borborema.pb.gov.br"]
    BASE_URL = "https://www.borborema.pb.gov.br"
    start_date = date(2023, 10, 2)
