from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAltoAlegreSpider(BaseInstarSpider):
    TERRITORY_ID = "3501103"
    name = "sp_alto_alegre"
    allowed_domains = ["altoalegre.sp.gov.br"]
    start_date = date(2018, 7, 3)
    base_url = "http://www.altoalegre.sp.gov.br/portal/diario-oficial"
