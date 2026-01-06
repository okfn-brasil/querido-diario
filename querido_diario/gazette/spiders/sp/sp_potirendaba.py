from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPotirendabaSpider(BaseInstarSpider):
    TERRITORY_ID = "3540804"
    name = "sp_potirendaba"
    base_url = "https://www.potirendaba.sp.gov.br/portal/diario-oficial"
    start_date = date(2024, 1, 21)
