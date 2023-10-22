from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAndradinaSpider(BaseInstarSpider):
    TERRITORY_ID = "3514403"
    name = "sp_dracena"
    allowed_domains = ["dracena.sp.gov.br"]
    base_url = "https://www.dracena.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 11, 24)
