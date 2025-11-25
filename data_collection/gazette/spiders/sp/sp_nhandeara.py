from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpNhandearaSpider(BaseInstarSpider):
    TERRITORY_ID = "3532603"
    name = "sp_nhandeara"
    base_url = "https://www.nhandeara.sp.gov.br/portal/diario-oficial"
    start_date = date(2023, 8, 17)
