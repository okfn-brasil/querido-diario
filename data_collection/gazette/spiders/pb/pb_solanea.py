from datetime import date

from gazette.spiders.base.adiarios_v1 import BaseAdiariosV1Spider


class PbSolaneaSpider(BaseAdiariosV1Spider):
    TERRITORY_ID = "2516003"
    name = "pb_solanea"
    allowed_domains = ["solanea.pb.gov.br"]
    BASE_URL = "https://www.solanea.pb.gov.br"
    start_date = date(2021, 5, 13)
