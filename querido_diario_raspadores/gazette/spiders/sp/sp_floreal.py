from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpFlorealSpider(BaseInstarSpider):
    TERRITORY_ID = "3515905"
    name = "sp_floreal"
    base_url = "https://www.floreal.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 11, 9)
