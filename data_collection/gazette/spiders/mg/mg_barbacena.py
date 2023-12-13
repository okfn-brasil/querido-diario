from datetime import date
from gazette.spiders.base.instar import BaseInstarSpider

class MgCarmoDoRioClaroSpider(BaseInstarSpider):
    TERRITORY_ID = "3105608"
    name = "mg_barbacena"
    allowed_domains = ["barbacena.mg.gov.br"]
    base_url = "https://www1.barbacena.mg.gov.br/portal/diario-oficial"
    start_date = date(2013, 6, 5)
