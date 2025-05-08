from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpVeraCruzSpider(BaseInstarSpider):
    TERRITORY_ID = "3556602"
    name = "sp_vera_cruz"
    base_url = "https://www.veracruz.sp.gov.br/portal/diario-oficial"
    start_date = date(2018, 2, 1)
