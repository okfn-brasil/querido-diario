from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbCajazeirasSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2503704"
    name = "pb_cajazeiras"
    allowed_domains = ["cajazeiras.pb.gov.br"]
    BASE_URL = "https://www.cajazeiras.pb.gov.br"
    start_date = date(2017, 2, 2)
