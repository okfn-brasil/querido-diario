from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIrapuruSpider(BaseInstarSpider):
    TERRITORY_ID = "3521606"
    name = "sp_irapuru"
    base_url = "http://www.irapuru.sp.gov.br/portal/diario-oficial"
    start_date = date(2023, 3, 10)
