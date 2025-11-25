from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpNovaLuzitaniaSpider(BaseInstarSpider):
    TERRITORY_ID = "3533304"
    name = "sp_nova_luzitania"
    base_url = "https://www.novaluzitania.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 10, 31)
