from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpLagoinhaSpider(BaseInstarSpider):
    TERRITORY_ID = "3526308"
    name = "sp_lagoinha"
    base_url = "https://www.lagoinha.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 11, 25)
