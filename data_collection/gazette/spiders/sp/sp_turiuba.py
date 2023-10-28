from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpTuriubaSpider(BaseInstarSpider):
    TERRITORY_ID = "3555208"
    name = "sp_turiuba"
    allowed_domains = ["turiuba.sp.gov.br"]
    base_url = "https://www.turiuba.sp.gov.br/portal/diario-oficial"
    start_date = date(2020, 6, 19)
