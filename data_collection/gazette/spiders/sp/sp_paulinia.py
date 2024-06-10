from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPauliniaSpider(BaseInstarSpider):
    TERRITORY_ID = "3536505"
    name = "sp_paulinia"
    allowed_domains = ["paulinia.sp.gov.br"]
    base_url = "https://www.paulinia.sp.gov.br/portal/diario-oficial"
    start_date = date(2012, 1, 4)
