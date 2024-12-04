from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpTaquaralSpider(BaseInstarSpider):
    TERRITORY_ID = "3553658"
    name = "sp_taquaral"
    allowed_domains = ["taquaral.sp.gov.br"]
    base_url = "https://www.taquaral.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 1, 3)
