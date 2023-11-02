from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpParisiSpider(BaseInstarSpider):
    TERRITORY_ID = "3536257"
    name = "sp_parisi"
    allowed_domains = ["parisi.sp.gov.br"]
    start_date = date(2015, 2, 27)
    base_url = "https://www.parisi.sp.gov.br/portal/diario-oficial"
