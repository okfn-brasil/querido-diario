from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMonteMorSpider(BaseInstarSpider):
    TERRITORY_ID = "3531803"
    name = "sp_monte_mor"
    allowed_domains = ["montemor.sp.gov.br"]
    base_url = "https://www.montemor.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 9, 20)
