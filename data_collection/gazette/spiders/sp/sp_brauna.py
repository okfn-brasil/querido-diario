from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpBraunaSpider(BaseInstarSpider):
    TERRITORY_ID = "3507704"
    name = "sp_brauna"
    allowed_domains = ["brauna.sp.gov.br"]
    base_url = "https://www.brauna.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 2, 12)
