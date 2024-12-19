import datetime

from gazette.spiders.base.deto import BaseDetoSpider


class ToCombinado(BaseDetoSpider):
    TERRITORY_ID = "1712157"
    name = "to_combinado"
    allowed_domains = ["combinado.to.gov.br"]
    start_date = datetime.date(2002, 3, 31)
    BASE_URL = "http://www.combinado.to.gov.br/transparencia"
