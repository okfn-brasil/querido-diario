from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIlhabelaSpider(BaseInstarSpider):
    TERRITORY_ID = "3520400"
    name = "sp_ilhabela"
    allowed_domains = ["ilhabela.sp.gov.br"]
    base_url = "https://www.ilhabela.sp.gov.br/portal/diario-oficial"
    start_date = date(2009, 1, 1)
