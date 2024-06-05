from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIacangaSpider(BaseInstarSpider):
    TERRITORY_ID = "3519105"
    name = "sp_iacanga"
    allowed_domains = ["iacanga.sp.gov.br"]
    base_url = "https://www.iacanga.sp.gov.br/portal/diario-oficial"
    start_date = date(2014, 1, 9)
