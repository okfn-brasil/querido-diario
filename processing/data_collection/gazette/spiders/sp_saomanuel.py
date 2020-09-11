from gazette.spiders.instar_base import BaseInstarSpider


class SpSaoManuelSpider(BaseInstarSpider):
    TERRITORY_ID = "3550100"
    name = "sp_saomanuel"
    allowed_domains = ["saomanuel.sp.gov.br"]
    start_urls = ["https://www.saomanuel.sp.gov.br/portal/diario-oficial"]
