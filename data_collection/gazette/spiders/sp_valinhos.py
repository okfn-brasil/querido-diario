import datetime

from gazette.spiders.base.instar import BaseInstarSpider


class SpValinhosSpider(BaseInstarSpider):
    TERRITORY_ID = "3556206"
    name = "sp_valinhos"
    allowed_domains = ["valinhos.sp.gov.br"]
    base_url = "https://www.valinhos.sp.gov.br/portal/diario-oficial"
    start_date = datetime.date(2004, 12, 12)
