from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPalmitalSpider(BaseInstarSpider):
    TERRITORY_ID = "3535309"
    name = "sp_palmital"
    base_url = "https://www.palmital.sp.gov.br/portal/diario-oficial"
    start_date = date(2005, 6, 11)
