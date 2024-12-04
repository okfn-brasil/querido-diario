from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPrataniaSpider(BaseInstarSpider):
    TERRITORY_ID = "3541059"
    name = "sp_pratania"
    allowed_domains = ["pratania.sp.gov.br"]
    start_date = date(2019, 5, 13)
    base_url = "https://www.pratania.sp.gov.br/portal/diario-oficial"
