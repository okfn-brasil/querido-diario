from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpUniaoPaulistaSpider(BaseInstarSpider):
    TERRITORY_ID = "3555703"
    name = "sp_uniao_paulista"
    allowed_domains = ["uniaopaulista.sp.gov.br"]
    base_url = "https://uniaopaulista.sp.gov.br/portal/diario-oficial"
    start_date = date(2023, 1, 11)
