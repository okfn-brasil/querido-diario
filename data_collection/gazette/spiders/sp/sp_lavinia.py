from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpLaviniaSpider(BaseInstarSpider):
    TERRITORY_ID = "3526506"
    name = "sp_lavinia"
    allowed_domains = ["lavinia.sp.gov.br"]
    base_url = "https://www.lavinia.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 2, 21)
