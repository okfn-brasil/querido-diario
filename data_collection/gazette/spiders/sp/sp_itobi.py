from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpItobiSpider(BaseInstarSpider):
    TERRITORY_ID = "3523800"
    name = "sp_itobi"
    allowed_domains = ["itobi.sp.gov.br"]
    base_url = "https://www.itobi.sp.gov.br/portal/diario-oficial"
    start_date = date(2011, 4, 1)
