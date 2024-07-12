from datetime import date

from gazette.spiders.base.instar import BaseInstarSpider


class MsMaracajuSpider(BaseInstarSpider):
    TERRITORY_ID = "5005400"
    name = "ms_maracaju"
    allowed_domains = ["maracaju.ms.gov.br"]
    base_url = "https://www.maracaju.ms.gov.br/portal/diario-oficial"
    start_date = date(2013, 3, 14)
