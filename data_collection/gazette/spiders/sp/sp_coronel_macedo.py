from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpCoronelMacedoSpider(BaseInstarSpider):
    TERRITORY_ID = "3512605"
    name = "sp_coronel_macedo"
    allowed_domains = ["coronelmacedo.sp.gov.br"]
    base_url = "https://www.coronelmacedo.sp.gov.br/portal/diario-oficial"
    start_date = date(2017, 5, 29)
