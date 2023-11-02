from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPontesGestalSpider(BaseInstarSpider):
    TERRITORY_ID = "3540309"
    name = "sp_pontes_gestal"
    allowed_domains = ["pontesgestal.sp.gov.br"]
    base_url = "https://www.pontesgestal.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 7, 14)
