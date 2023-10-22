from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpPresidenteEpitacioSpider(BaseInstarSpider):
    TERRITORY_ID = "3541307"
    name = "sp_presidente_epitacio"
    allowed_domains = ["presidenteepitacio.sp.gov.br"]
    base_url = "https://www.presidenteepitacio.sp.gov.br/portal/diario-oficial"
    start_date = date(2019, 10, 18)
