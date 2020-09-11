from gazette.spiders.instar_base import BaseInstarSpider


class SpAltoAlegreSpider(BaseInstarSpider):
    TERRITORY_ID = "3501103"
    name = "sp_altoalegre"
    allowed_domains = ["altoalegre.sp.gov.br"]
    start_urls = ["http://www.altoalegre.sp.gov.br/portal/diario-oficial"]
