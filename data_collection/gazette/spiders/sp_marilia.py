from gazette.spiders.base.instar import BaseInstarSpider


class SpMariliaSpider(BaseInstarSpider):
    TERRITORY_ID = "3529005"
    name = "sp_marilia"
    allowed_domains = ["marilia.sp.gov.br"]
    start_urls = ["https://www.marilia.sp.gov.br/portal/diario-oficial"]
