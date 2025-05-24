from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpItapuiSpider(BaseInstarSpider):
    TERRITORY_ID = "3522901"
    name = "sp_itapui"
    base_url = "https://www.itapui.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 12, 15)
