from gazette.spiders.instar_base import BaseInstarSpider


class SpSantaErnestinaPaulistaSpider(BaseInstarSpider):
    TERRITORY_ID = "3546504"
    name = "sp_santaernestina"
    allowed_domains = ["santaernestina.sp.gov.br"]
    start_urls = ["https://www.santaernestina.sp.gov.br/portal/diario-oficial"]
