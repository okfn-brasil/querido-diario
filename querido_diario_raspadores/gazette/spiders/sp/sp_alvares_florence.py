from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAlvaresFlorenceSpider(BaseInstarSpider):
    TERRITORY_ID = "3501202"
    name = "sp_alvares_florence"
    base_url = "https://www.alvaresflorence.sp.gov.br/portal/diario-oficial"
    start_date = date(2013, 3, 13)
