from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpMoncoesSpider(BaseInstarSpider):
    TERRITORY_ID = "3531001"
    name = "sp_moncoes"
    base_url = "https://www.moncoes.sp.gov.br/portal/diario-oficial"
    start_date = date(2024, 1, 12)
