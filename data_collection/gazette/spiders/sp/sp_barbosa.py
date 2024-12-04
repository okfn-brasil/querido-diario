from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpBarbosaSpider(BaseInstarSpider):
    TERRITORY_ID = "3505104"
    name = "sp_barbosa"
    allowed_domains = ["barbosa.sp.gov.br"]
    base_url = "https://www.barbosa.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 1, 21)
