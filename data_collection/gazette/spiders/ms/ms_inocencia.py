from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MsInocenciaSpider(BaseInstarSpider):
    TERRITORY_ID = "5004403"
    name = "ms_inocencia"
    base_url = "https://www.inocencia.ms.gov.br/portal/diario-oficial"
    start_date = date(2013, 10, 17)
