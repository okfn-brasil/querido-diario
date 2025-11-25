from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MgNovaSerranaSpider(BaseInstarSpider):
    TERRITORY_ID = "3145208"
    name = "mg_nova_serrana"
    base_url = "https://www.novaserrana.mg.gov.br/portal/diario-oficial"
    start_date = date(2015, 10, 27)
