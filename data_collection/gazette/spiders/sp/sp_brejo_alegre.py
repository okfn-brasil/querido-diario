from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpBrejoAlegreSpider(BaseInstarSpider):
    TERRITORY_ID = "3507753"
    name = "sp_brejo_alegre"
    allowed_domains = ["brejoalegre.sp.gov.br"]
    base_url = "https://www.brejoalegre.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 10, 21)
