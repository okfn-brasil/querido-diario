from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class SpGeneralSalgadoSpider(BaseInstarSpider):
    TERRITORY_ID = "3516903"
    name = "sp_general_salgado"
    allowed_domains = ["generalsalgado.sp.gov.br"]
    base_url = "https://www.generalsalgado.sp.gov.br/portal/diario-oficial"
    start_date = date(2022, 1, 13)
