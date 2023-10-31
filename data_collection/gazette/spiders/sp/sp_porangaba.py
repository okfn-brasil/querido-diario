from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPorangabaSpider(BaseInstarSpider):
    TERRITORY_ID = "3540507"
    name = "sp_porangaba"
    allowed_domains = ["porangaba.sp.gov.br"]
    base_url = "https://www.porangaba.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 10, 6)
