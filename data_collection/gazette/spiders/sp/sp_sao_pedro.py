from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpSaoPedroSpider(BaseInstarSpider):
    TERRITORY_ID = "3550407"
    name = "sp_sao_pedro"
    base_url = "https://www.saopedro.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 5, 25)
