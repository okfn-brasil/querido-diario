from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPenapolisSpider(BaseInstarSpider):
    TERRITORY_ID = "3537305"
    name = "sp_penapolis"
    allowed_domains = ["penapolis.sp.gov.br"]
    base_url = "https://www.penapolis.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 1, 3)
