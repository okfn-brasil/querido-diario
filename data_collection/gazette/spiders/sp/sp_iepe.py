from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIepeSpider(BaseInstarSpider):
    TERRITORY_ID = "3519907"
    name = "sp_iepe"
    allowed_domains = ["iepe.sp.gov.br"]
    base_url = "https://www.iepe.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 10, 16)
