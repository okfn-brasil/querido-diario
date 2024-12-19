import datetime

from gazette.spiders.base.deto import BaseDetoSpider


class ToAuroraDoTocantins(BaseDetoSpider):
    TERRITORY_ID = "1712157"
    name = "to_auroradotocantins"
    allowed_domains = ["auroradotocantins.to.gov.br"]
    start_date = datetime.date(2002, 3, 31)
    BASE_URL = "http://www.auroradotocantins.to.gov.br/transparencia"
