from datetime import date

from gazette.spiders.base.dionet import BaseDionetSpider


class MsCorumba(BaseDionetSpider):
    TERRITORY_ID = "5003207"
    name = "ms_corumba"
    allowed_domains = ["do.corumba.ms.gov.br"]
    start_date = date(2012, 6, 26)

    BASE_URL = "https://do.corumba.ms.gov.br"
