from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgTaiobeirasSpider(BaseInstarSpider):
    TERRITORY_ID = "3168002"
    name = "mg_taiobeiras"
    allowed_domains = ["taiobeiras.mg.gov.br"]
    base_url = "https://www.taiobeiras.mg.gov.br/portal/diario-oficial"
    start_date = date(2022, 12, 31)
