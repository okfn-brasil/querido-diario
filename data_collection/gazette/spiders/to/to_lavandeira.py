import datetime

from gazette.spiders.base.deto import BaseDetoSpider


class ToLavandeira(BaseDetoSpider):
    TERRITORY_ID = "1712157"
    name = "to_lavandeira"
    allowed_domains = ["lavandeira.to.gov.br"]
    start_date = datetime.date(2002, 3, 31)
    BASE_URL = "https://www.lavandeira.to.gov.br/transparencia"
