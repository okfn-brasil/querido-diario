from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpNipoaSpider(BaseInstarSpider):
    TERRITORY_ID = "3532702"
    name = "sp_nipoa"
    base_url = "https://www.nipoa.sp.gov.br/portal/diario-oficial"
    start_date = date(2025, 10, 28)
