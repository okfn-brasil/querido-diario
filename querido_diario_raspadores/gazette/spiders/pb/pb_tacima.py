from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbTacimaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2516409"
    name = "pb_tacima"
    allowed_domains = ["pmtacima.pb.gov.br"]
    BASE_URL = "https://www.pmtacima.pb.gov.br"
    start_date = date(2024, 1, 26)
