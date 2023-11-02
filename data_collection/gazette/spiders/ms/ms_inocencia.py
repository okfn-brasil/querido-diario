import datetime

from gazette.spiders.base.instar import BaseInstarSpider


class MsInocenciaSpider(BaseInstarSpider):
    TERRITORY_ID = "5004403"
    name = "ms_inocencia"
    allowed_domains = ["inocencia.ms.gov.br"]
    base_url = "https://www.inocencia.ms.gov.br/portal/diario-oficial"
    start_date = datetime.date(2013, 10, 17)  # edition_number 01
