from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMacaubalSpider(BaseInstarSpider):
    TERRITORY_ID = "3528106"
    name = "sp_macaubal"
    base_url = "https://macaubal.sp.gov.br/portal/diario-oficial"
    start_date = date(2023, 6, 21)
