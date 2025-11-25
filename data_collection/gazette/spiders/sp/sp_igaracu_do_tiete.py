from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpIgaracuDoTieteSpider(BaseInstarSpider):
    TERRITORY_ID = "3520004"
    name = "sp_igaracu_do_tiete"
    base_url = "https://www.igaracudotiete.sp.gov.br/portal/diario-oficial"
    start_date = date(2021, 1, 1)
