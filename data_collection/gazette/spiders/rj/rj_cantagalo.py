from datetime import date

from gazette.spiders.base.rgsites import BaseRgSites


class RjCantagaloSpider(BaseRgSites):
    name = "rj_cantagalo"
    TERRITORY_ID = "3301108"
    allowed_domains = ["www.cantagalo.rj.gov.br"]
    BASE_URL = "https://www.cantagalo.rj.gov.br/transparencia/diario-oficial"
    start_date = date(2018, 3, 26)
