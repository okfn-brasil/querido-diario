from gazette.spiders.instar_base import BaseInstarSpider


class SpCoronelMacedoSpider(BaseInstarSpider):
    TERRITORY_ID = "3512605"
    name = "sp_coronelmacedo"
    allowed_domains = ["coronelmacedo.sp.gov.br"]
    start_urls = ["https://www.coronelmacedo.sp.gov.br/portal/diario-oficial"]
