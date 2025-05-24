from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpTerraRoxaSpider(BaseInstarSpider):
    TERRITORY_ID = "3554409"
    name = "sp_terra_roxa"
    base_url = "https://www.terraroxa.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 6, 29)
