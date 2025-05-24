from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgCampoBeloSpider(BaseInstarSpider):
    TERRITORY_ID = "3111200"
    name = "mg_campo_belo"
    base_url = "https://www.campobelo.mg.gov.br/portal/diario-oficial"
    start_date = date(2016, 1, 5)
