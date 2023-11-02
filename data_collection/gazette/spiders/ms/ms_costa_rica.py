from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MsCostaRicaSpider(BaseInstarSpider):
    TERRITORY_ID = "5003256"
    name = "ms_costa_rica"
    allowed_domains = ["costarica.ms.gov.br"]
    base_url = "https://www.costarica.ms.gov.br/portal/diario-oficial"
    start_date = date(2005, 1, 3)
