from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpAparecidaSpider(BaseInstarSpider):
    TERRITORY_ID = "3502507"
    name = "sp_aparecida"
    allowed_domains = ["aparecida.sp.gov.br"]
    base_url = "https://www.aparecida.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 3, 23)
