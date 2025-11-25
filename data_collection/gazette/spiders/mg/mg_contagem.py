from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgContagemSpider(BaseInstarSpider):
    TERRITORY_ID = "3118601"
    name = "mg_contagem"
    base_url = "https://portal.contagem.mg.gov.br/portal/diario-oficial"
    start_date = date(2005, 1, 31)
