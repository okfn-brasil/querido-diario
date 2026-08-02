from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpOurinhosSpider(BaseInstarSpider):
    TERRITORY_ID = "3534708"
    name = "sp_ourinhos"
    base_url = "https://www.ourinhos.sp.gov.br/portal/diario-oficial"
    start_date = date(2005, 1, 20)
