from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpVinhedoSpider(BaseInstarSpider):
    TERRITORY_ID = "3556701"
    name = "sp_vinhedo"
    base_url = "https://www.vinhedo.sp.gov.br/portal/diario-oficial"
    start_date = date(2010, 12, 9)
