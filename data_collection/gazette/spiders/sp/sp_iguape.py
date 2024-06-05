from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIguapeSpider(BaseInstarSpider):
    TERRITORY_ID = "3520301"
    name = "sp_iguape"
    allowed_domains = ["iguape.sp.gov.br"]
    base_url = "https://www.iguape.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 3, 2)
